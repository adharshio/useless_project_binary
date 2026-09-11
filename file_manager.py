"""
Windows De-fender — File Manager Module
Handles safe file operations: moving files to Deleted_Safe_Files or Threat_Museum.

SAFETY:
- NEVER permanently deletes any file.
- NEVER executes any file.
- Only moves/copies files to designated directories.
"""

import shutil
from pathlib import Path
from datetime import datetime

# Designated directories
DATA_DIR = Path(__file__).parent / "data"
DELETED_DIR = DATA_DIR / "Deleted_Safe_Files"
MUSEUM_DIR = DATA_DIR / "Threat_Museum"


def ensure_directories():
    """Create all required data directories if they don't exist."""
    DELETED_DIR.mkdir(parents=True, exist_ok=True)
    MUSEUM_DIR.mkdir(parents=True, exist_ok=True)


def _unique_name(directory: Path, filename: str) -> Path:
    """
    Generate a unique filename in the target directory to avoid overwrites.
    Appends a timestamp if the file already exists.
    """
    target = directory / filename
    if not target.exists():
        return target

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"{stem}_{timestamp}{suffix}"
    return directory / new_name


def move_to_deleted(filepath: str) -> str:
    """
    Move a 'clean' file to the Deleted_Safe_Files directory.

    Args:
        filepath: Path to the file to move.

    Returns:
        The destination path as a string.

    Raises:
        FileNotFoundError: If the source file doesn't exist.
    """
    ensure_directories()
    source = Path(filepath)

    if not source.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    dest = _unique_name(DELETED_DIR, source.name)
    shutil.move(str(source), str(dest))
    return str(dest)


def move_to_museum(filepath: str) -> str:
    """
    Copy a 'demo threat' file to the Threat_Museum directory.
    Uses copy (not move) so the original demo file can be reused.

    Args:
        filepath: Path to the file to copy.

    Returns:
        The destination path as a string.

    Raises:
        FileNotFoundError: If the source file doesn't exist.
    """
    ensure_directories()
    source = Path(filepath)

    if not source.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    dest = _unique_name(MUSEUM_DIR, source.name)
    shutil.copy2(str(source), str(dest))
    return str(dest)


def get_deleted_dir() -> Path:
    """Return the Deleted_Safe_Files directory path."""
    return DELETED_DIR


def get_museum_dir() -> Path:
    """Return the Threat_Museum directory path."""
    return MUSEUM_DIR
