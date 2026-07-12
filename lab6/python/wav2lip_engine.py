"""Wav2Lip as a third renderer for Digital Human Studio (Lab 6).

Why a subprocess instead of importing Wav2Lip into this app's environment:
Wav2Lip is a 2020 codebase pinned to old torch/librosa/opencv versions, and MuseTalk
needs newer ones. Forcing both into one virtualenv is a fight nobody wins. Lab 7 already
has a *working* Wav2Lip install with its own venv, so we call that — the environments stay
isolated and neither model has to move.

Paths can be overridden with WAV2LIP_DIR / WAV2LIP_PY; the defaults find Lab 7 from here.
"""

from __future__ import annotations

import os
import shutil
import sys
import subprocess
from pathlib import Path

_HERE = Path(__file__).resolve().parent


def _default_dir() -> Path:
    """Wav2Lip lives next to this app (python/wav2lip). If the app is checked out
    inside a repo that already has an install — e.g. an n8n course that keeps one for
    a different lab — reuse that rather than downloading the checkpoint twice."""
    for parent in _HERE.parents:
        shared = parent / "lab7-opensource" / "service" / "wav2lip"
        if (shared / "checkpoints" / "wav2lip_gan.pth").exists():
            return shared
    return _HERE / "wav2lip"


def _default_python() -> Path:
    """Wav2Lip is pinned to old torch/librosa versions that fight with MuseTalk's, so it
    gets its own virtualenv where one exists. Otherwise fall back to the running one."""
    d = _default_dir()
    for cand in (d.parent / ".venv" / "bin" / "python", _HERE / ".venv" / "bin" / "python"):
        if cand.exists():
            return cand
    return Path(sys.executable)


WAV2LIP_DIR = Path(os.environ.get("WAV2LIP_DIR", _default_dir()))
WAV2LIP_PY = Path(os.environ.get("WAV2LIP_PY", _default_python()))
CHECKPOINT = WAV2LIP_DIR / "checkpoints" / "wav2lip_gan.pth"


def available() -> bool:
    """True only if every piece is present — the UI greys the button out otherwise,
    rather than offering a render that fails a minute later."""
    return (
        WAV2LIP_PY.exists()
        and (WAV2LIP_DIR / "inference.py").exists()
        and CHECKPOINT.exists()
    )


def render(image: str, audio: str, out_mp4: str, progress=None) -> None:
    """Lip-sync `image` to `audio` with Wav2Lip, then normalise to 1080p."""
    def say(msg, pct):
        if progress:
            progress(msg, pct)

    if not available():
        raise RuntimeError(
            "Wav2Lip is not installed. Expected the Lab 7 install at "
            f"{WAV2LIP_DIR} with checkpoints/wav2lip_gan.pth, and its venv python at {WAV2LIP_PY}."
        )

    raw = out_mp4 + ".raw.mp4"
    say("running Wav2Lip (96x96 mouth model — fast)", 10)

    # Same invocation Lab 7 uses, which is known to work on this machine.
    proc = subprocess.run(
        [
            str(WAV2LIP_PY), "inference.py",
            "--checkpoint_path", "checkpoints/wav2lip_gan.pth",
            "--face", str(Path(image).resolve()),
            "--audio", str(Path(audio).resolve()),
            "--outfile", str(Path(raw).resolve()),
            "--resize_factor", "1",
            "--nosmooth",
            "--pads", "0", "15", "0", "0",
        ],
        cwd=str(WAV2LIP_DIR),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0 or not Path(raw).exists():
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-6:]
        raise RuntimeError("Wav2Lip failed:\n" + "\n".join(tail))

    say("normalising to 1080p", 85)
    ff = shutil.which("ffmpeg") or "ffmpeg"
    subprocess.run(
        [
            ff, "-y", "-i", raw,
            "-vf",
            "scale=1920:1080:force_original_aspect_ratio=decrease,"
            "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", out_mp4,
        ],
        check=True,
        capture_output=True,
    )
    Path(raw).unlink(missing_ok=True)
    say("done", 100)
