"""Photoreal lip sync with MuseTalk, on Apple Silicon.

MuseTalk inpaints the mouth region of a face in the VAE's latent space,
conditioned on Whisper audio features. This module drives the official model
weights but replaces one piece of the official pipeline: the DWPose/mmpose
landmark step.

Why: mmpose pulls in mmcv, which has no Apple Silicon wheels and is a miserable
source build. All MuseTalk actually needs from it is a face bounding box derived
from 68 face landmarks — and we already run MediaPipe's 478-point mesh in the
browser for the rig. So we compute the same box from MediaPipe here, and the
model is none the wiser: the crop it receives has the same geometry it was
trained on.

The box MuseTalk wants (see preprocessing.get_landmark_and_bbox upstream):
    x1 = leftmost face landmark      x2 = rightmost face landmark
    y2 = lowest face landmark (chin)
    y1 = nose_bridge_y - (y2 - nose_bridge_y)
i.e. vertically symmetric about the mid-nose point, so the crop is centred on the
mouth half of the face. `bbox_shift` nudges that nose point up or down, which is
MuseTalk's standard quality knob.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
import torch

HERE = Path(__file__).parent
REPO = HERE / "repo"
MODELS = HERE / "models"

# MuseTalk imports its own modules by bare name (`from face_detection import ...`),
# so its package roots have to be on sys.path before we touch it.
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "musetalk" / "utils"))


def pick_device() -> torch.device:
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


# MediaPipe mesh indices standing in for the 68-point landmarks MuseTalk uses.
# 4 is the nose tip; 5 sits on the lower nose bridge, which is the closest analogue
# of dlib's point 29 (the one upstream calls `half_face_coord`).
MP_NOSE_BRIDGE = 5
# The face oval — the outline MuseTalk measures its box against. Using the whole
# 478-point mesh would include the irises and skew nothing, but the oval is exactly
# the silhouette, so min/max over it is the crisp equivalent of the 68-point hull.
MP_FACE_OVAL = [
    10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378,
    400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21,
    54, 103, 67, 109,
]


class MuseTalkEngine:
    """Loads once, renders many. Model load is ~10s; keep the instance alive."""

    def __init__(self, device: torch.device | None = None, version: str = "v15"):
        self.device = device or pick_device()
        self.version = version
        self._loaded = False

    # ── model loading ────────────────────────────────────────────────────
    def load(self) -> None:
        if self._loaded:
            return

        from musetalk.utils.utils import load_all_model
        from musetalk.utils.audio_processor import AudioProcessor
        from musetalk.utils.face_parsing import FaceParsing
        from transformers import WhisperModel

        # PyTorch 2.6+ defaults torch.load(weights_only=True), which cannot read the
        # legacy-tar checkpoints MuseTalk and BiSeNet ship. These files came from
        # pytorch.org and HuggingFace and we downloaded them ourselves, so unpickling
        # them is a risk we've already taken — but scope the patch to model loading
        # rather than leaving it on process-wide.
        _orig_load = torch.load

        def _load(*a, **kw):
            kw.setdefault("weights_only", False)
            return _orig_load(*a, **kw)

        torch.load = _load

        cwd = os.getcwd()
        os.chdir(REPO)  # both load_all_model and FaceParsing resolve ./models relative to CWD
        try:
            self.vae, self.unet, self.pe = load_all_model(
                unet_model_path=str(MODELS / "musetalkV15" / "unet.pth"),
                vae_type="sd-vae",
                unet_config=str(MODELS / "musetalkV15" / "musetalk.json"),
                device=self.device,
            )
            self.face_parser = FaceParsing(left_cheek_width=90, right_cheek_width=90)
        finally:
            os.chdir(cwd)
            torch.load = _orig_load

        # fp16 is a CUDA habit; MPS is happiest in fp32 and the model is small.
        self.unet.model = self.unet.model.to(self.device).float()
        self.pe = self.pe.to(self.device).float()
        self.vae.vae = self.vae.vae.to(self.device).float()
        # The repo's VAE wrapper picks its own device — `cuda if available else cpu` —
        # so on a Mac it silently sits on the CPU and then hands CPU tensors to an MPS
        # UNet. Point it at the real device.
        self.vae.device = self.device
        self.weight_dtype = torch.float32
        self.timesteps = torch.tensor([0], device=self.device)

        self.audio_processor = AudioProcessor(feature_extractor_path=str(MODELS / "whisper"))
        self.whisper = (
            WhisperModel.from_pretrained(str(MODELS / "whisper"))
            .to(device=self.device, dtype=self.weight_dtype)
            .eval()
        )
        self.whisper.requires_grad_(False)

        # The same face_landmarker.task the browser uses, so the Python renderer and
        # the live preview agree on where the face is.
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision

        model_file = HERE.parent / "vendor" / "face_landmarker.task"
        self.landmarker = vision.FaceLandmarker.create_from_options(
            vision.FaceLandmarkerOptions(
                base_options=mp_python.BaseOptions(model_asset_path=str(model_file)),
                running_mode=vision.RunningMode.IMAGE,
                num_faces=1,
            )
        )
        self._loaded = True

    # ── the mmpose replacement ───────────────────────────────────────────
    def face_bbox(self, frame_bgr: np.ndarray, bbox_shift: int = 0):
        """MuseTalk's crop box, computed from MediaPipe instead of DWPose."""
        import mediapipe as mp

        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        res = self.landmarker.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
        if not res.face_landmarks:
            return None

        lm = res.face_landmarks[0]
        oval = np.array([[lm[i].x * w, lm[i].y * h] for i in MP_FACE_OVAL])

        x1, x2 = int(oval[:, 0].min()), int(oval[:, 0].max())
        y2 = int(oval[:, 1].max())                       # chin
        nose_y = int(lm[MP_NOSE_BRIDGE].y * h) + bbox_shift

        half = y2 - nose_y                               # nose → chin
        y1 = max(0, nose_y - half)                       # mirror it upward

        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        if x2 - x1 <= 0 or y2 - y1 <= 0:
            return None
        return x1, y1, x2, y2

    # ── inference ────────────────────────────────────────────────────────
    @torch.no_grad()
    def render(
        self,
        image_path: str,
        audio_path: str,
        out_path: str,
        fps: int = 25,
        bbox_shift: int = 0,
        batch_size: int = 4,
        progress=None,
    ) -> str:
        self.load()
        from musetalk.utils.blending import get_image
        from musetalk.utils.utils import datagen

        def say(msg, pct):
            if progress:
                progress(msg, pct)

        say("reading image", 2)
        frame = cv2.imread(image_path)
        if frame is None:
            raise ValueError("Could not read the portrait image.")

        # Odd dimensions break the VAE's downsampling; keep it even and sane.
        max_side = 1024
        if max(frame.shape[:2]) > max_side:
            s = max_side / max(frame.shape[:2])
            frame = cv2.resize(frame, (int(frame.shape[1] * s) // 2 * 2,
                                       int(frame.shape[0] * s) // 2 * 2))

        bbox = self.face_bbox(frame, bbox_shift)
        if bbox is None:
            raise ValueError("No face found in the portrait.")
        x1, y1, x2, y2 = bbox

        say("encoding audio with whisper", 8)
        features, librosa_len = self.audio_processor.get_audio_feature(audio_path)
        chunks = self.audio_processor.get_whisper_chunk(
            features, self.device, self.weight_dtype, self.whisper,
            librosa_len, fps=fps, audio_padding_length_left=2, audio_padding_length_right=2,
        )
        n_frames = len(chunks)
        if n_frames == 0:
            raise ValueError("The audio produced no frames — is it silent or empty?")

        say("encoding the face", 14)
        crop = frame[y1:y2, x1:x2]
        crop_256 = cv2.resize(crop, (256, 256), interpolation=cv2.INTER_LANCZOS4)
        latents = self.vae.get_latents_for_unet(crop_256)  # masked + ref, 8 channels

        # A still portrait is one frame reused for every step of the audio.
        frame_list = [frame.copy()]
        coord_list = [bbox]
        latent_list = [latents]

        say(f"generating {n_frames} frames", 20)
        gen = datagen(
            whisper_chunks=chunks,
            vae_encode_latents=latent_list * n_frames,
            batch_size=batch_size,
            delay_frame=0,
            device=self.device,
        )

        results = []
        done = 0
        for whisper_batch, latent_batch in gen:
            audio_feat = self.pe(whisper_batch.to(dtype=self.weight_dtype))
            latent_batch = latent_batch.to(dtype=self.weight_dtype)

            pred = self.unet.model(
                latent_batch, self.timesteps, encoder_hidden_states=audio_feat
            ).sample
            recon = self.vae.decode_latents(pred)

            for face in recon:
                results.append(face)
                done += 1
            say(f"generating frames ({done}/{n_frames})", 20 + int(65 * done / n_frames))

        say("compositing", 88)
        tmp = Path(tempfile.mkdtemp(prefix="musetalk-"))
        for i, face in enumerate(results):
            resized = cv2.resize(face.astype(np.uint8), (x2 - x1, y2 - y1))
            # get_image() feathers the generated mouth back in using the face-parsing
            # mask, so the seam around the jaw doesn't show.
            combined = get_image(frame.copy(), resized, [x1, y1, x2, y2], mode="jaw", fp=self.face_parser)
            cv2.imwrite(str(tmp / f"{i:08d}.png"), combined)

        say("encoding video", 95)
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-framerate", str(fps), "-i", str(tmp / "%08d.png"),
             "-i", audio_path,
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
             "-c:a", "aac", "-shortest", out_path],
            check=True,
        )
        for p in tmp.glob("*.png"):
            p.unlink()
        tmp.rmdir()

        say("done", 100)
        return out_path


_engine: MuseTalkEngine | None = None


def get_engine() -> MuseTalkEngine:
    global _engine
    if _engine is None:
        _engine = MuseTalkEngine()
    return _engine
