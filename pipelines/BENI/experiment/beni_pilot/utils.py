from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

from pipelines.shared.data import set_seed as shared_set_seed
from pipelines.shared.io import (
    ensure_dirs as shared_ensure_dirs,
)
from pipelines.shared.io import (
    write_json as shared_write_json,
)
from pipelines.shared.io import (
    zip_outputs as shared_zip_outputs,
)

# Re-export shared functions so call sites (eval.py, train.py, …)
# can continue to ``from utils import write_json``.
ensure_dirs = shared_ensure_dirs
write_json = shared_write_json

# Bangla-specific punctuation — shared's generic normalize_text would
# strip these too, but using an explicit list is more conservative
# and preserves any non-punctuation symbols that might appear in
# Bangla news text.
BANGLA_PUNCT_RE = re.compile(r"[\u0964\u0965।,;:!?\"'“”‘’()\[\]{}<>/\\|_=+*`~#@$%^&]")
SPACE_RE = re.compile(r"\s+")


def set_seed(seed: int) -> None:
    """Set random seeds for reproducibility."""
    shared_set_seed(seed, include_torch=True)


def normalize_text(text: str) -> str:
    """Bangla-specific text normalisation.

    Uses an explicit Bangla punctuation list for conservative cleaning,
    preserving any non-punctuation symbols that generic ``[^\\w\\s]``
    would strip.
    """
    text = str(text).replace("\ufeff", " ")
    text = BANGLA_PUNCT_RE.sub(" ", text)
    text = SPACE_RE.sub(" ", text)
    return text.strip()


def zip_outputs(output_dir: Path, prefix: str = "beni_results") -> Path:
    """Zip the output directory for easy download from Kaggle.

    Args:
        output_dir: Directory to zip.
        prefix: Prefix for the zip filename (default: beni_results).

    Returns:
        Path to the created zip archive.
    """
    return shared_zip_outputs(output_dir, prefix=f"{prefix}")


def zip_subdirs(output_dir: Path, subdirs: list[str], prefix: str = "beni_artifacts") -> Path:
    """Zip specific subdirectories of an output directory into one archive.

    Creates a single zip containing only the named subdirectories
    (e.g. ``[\"models\"]``, ``[\"reports\", \"index\"]``).
    Useful for separating large model weights from smaller analysis outputs.

    Args:
        output_dir: Parent directory containing the subdirectories.
        subdirs: Names of subdirectories to include in the zip.
        prefix: Prefix for the zip filename (default: beni_artifacts).

    Returns:
        Path to the created zip archive.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{prefix}_{timestamp}"
    archive_path = output_dir.parent / name

    # Stage subdirectories under a temp dir so shutil.make_archive
    # sees exactly what we want (one base_dir with only the selected subdirs).
    tmp_dir = output_dir / f".zip_stage_{timestamp}"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    for sd in subdirs:
        src = output_dir / sd
        if src.exists():
            shutil.copytree(src, tmp_dir / sd, dirs_exist_ok=True)

    shutil.make_archive(str(archive_path), "zip", tmp_dir)
    shutil.rmtree(tmp_dir)
    return Path(f"{archive_path}.zip")
