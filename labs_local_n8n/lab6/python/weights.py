"""In-app weight downloader for Lab 6.

Both render engines need weights that are far too big to commit:

  MuseTalk  ~3.5 GB  the UNet, an SD-VAE, whisper-tiny and a face-parsing net
  Wav2Lip   ~440 MB  the GAN checkpoint + the s3fd face detector

The terminal script (download_models.sh) still works, but a learner staring at a
greyed-out button should not have to find a shell to fix it — so the app can fetch
them itself, and report real progress while it does.

Everything is downloaded from the projects' own published sources (Hugging Face for
the model files, the MuseTalk GitHub repo for the code it resolves at runtime).
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

PY_DIR = Path(__file__).resolve().parent
MODELS = PY_DIR / "models"
REPO = PY_DIR / "repo"


# ── what "installed" means ────────────────────────────────────────────────────
def musetalk_ready() -> bool:
    return (MODELS / "musetalkV15" / "unet.pth").exists()


def wav2lip_dir() -> Path:
    """Single source of truth for where Wav2Lip lives — the engine reads this too."""
    import wav2lip_engine

    return wav2lip_engine.WAV2LIP_DIR


def wav2lip_ready() -> bool:
    d = wav2lip_dir()
    return (d / "checkpoints" / "wav2lip_gan.pth").exists() and (d / "inference.py").exists()


# ── downloads ────────────────────────────────────────────────────────────────
def _hf(repo_id: str, dest: Path, files: list[str], progress, base: float, span: float) -> None:
    """Pull specific files from a Hugging Face repo, reporting progress per file."""
    from huggingface_hub import hf_hub_download

    dest.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(files):
        progress(f"downloading {repo_id} · {name}", base + span * (i / max(1, len(files))))
        path = hf_hub_download(repo_id=repo_id, filename=name)
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy(path, target)


def download_musetalk(progress=lambda m, p: None) -> None:
    """~3.5 GB. The UNet alone is 3.4 GB, so this is slow on a hotel wifi."""
    progress("cloning the MuseTalk repo", 2)
    if not REPO.exists():
        subprocess.run(
            ["git", "clone", "--depth", "1", "https://github.com/TMElyralab/MuseTalk.git", str(REPO)],
            check=True, capture_output=True,
        )
    MODELS.mkdir(parents=True, exist_ok=True)
    # MuseTalk resolves ./models relative to its own repo folder.
    link = REPO / "models"
    if not link.exists():
        link.symlink_to(MODELS)

    _hf("TMElyralab/MuseTalk", MODELS,
        ["musetalkV15/musetalk.json", "musetalkV15/unet.pth"], progress, 5, 70)
    _hf("stabilityai/sd-vae-ft-mse", MODELS / "sd-vae",
        ["config.json", "diffusion_pytorch_model.bin"], progress, 75, 10)
    _hf("openai/whisper-tiny", MODELS / "whisper",
        ["config.json", "pytorch_model.bin", "preprocessor_config.json"], progress, 85, 8)

    progress("downloading the face-parsing net", 94)
    face = MODELS / "face-parse-bisent"
    face.mkdir(parents=True, exist_ok=True)
    resnet = face / "resnet18-5c106cde.pth"
    if not resnet.exists():
        subprocess.run(
            ["curl", "-fsSL", "https://download.pytorch.org/models/resnet18-5c106cde.pth",
             "-o", str(resnet)],
            check=True, capture_output=True,
        )
    _hf("ManyOtherFunctions/face-parse-bisent", face, ["79999_iter.pth"], progress, 96, 3)

    if not musetalk_ready():
        raise RuntimeError("Download finished but unet.pth is missing — check the network and retry.")
    progress("MuseTalk is ready — reload the page", 100)


def download_wav2lip(progress=lambda m, p: None) -> None:
    """~440 MB: the GAN checkpoint plus the s3fd face detector."""
    d = wav2lip_dir()
    progress("cloning the Wav2Lip repo", 3)
    if not (d / "inference.py").exists():
        d.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", "https://github.com/Rudrabha/Wav2Lip.git", str(d)],
            check=True, capture_output=True,
        )

    ckpt_dir = d / "checkpoints"
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    progress("downloading wav2lip_gan.pth (~400 MB)", 15)
    _hf("numz/wav2lip_studio", ckpt_dir, ["Wav2lip/wav2lip_gan.pth"], progress, 15, 60)
    # The repo expects it flat in checkpoints/.
    nested = ckpt_dir / "Wav2lip" / "wav2lip_gan.pth"
    if nested.exists():
        shutil.move(str(nested), str(ckpt_dir / "wav2lip_gan.pth"))
        shutil.rmtree(ckpt_dir / "Wav2lip", ignore_errors=True)

    progress("downloading the s3fd face detector", 80)
    sfd = d / "face_detection" / "detection" / "sfd"
    sfd.mkdir(parents=True, exist_ok=True)
    if not (sfd / "s3fd.pth").exists():
        _hf("camenduru/Wav2Lip", sfd, ["checkpoints/s3fd.pth"], progress, 82, 15)
        nested = sfd / "checkpoints" / "s3fd.pth"
        if nested.exists():
            shutil.move(str(nested), str(sfd / "s3fd.pth"))
            shutil.rmtree(sfd / "checkpoints", ignore_errors=True)

    if not wav2lip_ready():
        raise RuntimeError("Download finished but the checkpoint is missing — check the network and retry.")
    progress("Wav2Lip is ready — reload the page", 100)


DOWNLOADERS = {"musetalk": download_musetalk, "wav2lip": download_wav2lip}
