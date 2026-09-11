"""
Anti-Antivirus — File Manager Module
Handles safe file operations: moving files to deleted_safe_files or threat_museum.

SAFETY:
- NEVER permanently deletes any file during development.
- NEVER executes or opens any scanned/infected file.
- Handles duplicate filenames safely (test.txt, test_1.txt, test_2.txt).
- Never overwrites existing files.
- Operates strictly within controlled application data directories.
"""

import shutil
import os
import sys
from pathlib import Path

# Application directories
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
DELETED_DIR = DATA_DIR / "deleted_safe_files"
MUSEUM_DIR = DATA_DIR / "threat_museum"

# Also support legacy casing if folder already exists
LEGACY_DELETED_DIR = DATA_DIR / "Deleted_Safe_Files"
LEGACY_MUSEUM_DIR = DATA_DIR / "Threat_Museum"


def ensure_directories():
    """Create all required data directories if they don't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DELETED_DIR.mkdir(parents=True, exist_ok=True)
    MUSEUM_DIR.mkdir(parents=True, exist_ok=True)


def _unique_name(directory: Path, filename: str) -> Path:
    """
    Generate a unique target path in directory to avoid overwriting existing files.
    Sequence format:
        test.txt -> test_1.txt -> test_2.txt ...
    """
    target = directory / filename
    if not target.exists():
        return target

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        candidate = directory / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def move_to_deleted(filepath: str) -> str:
    """
    Move a 'clean' file to the deleted_safe_files directory.

    SAFETY:
    - Never permanently deletes the file.
    - Resolves collisions with unique numbered suffix.
    - Never executes the file.

    Args:
        filepath: Path to the file to move.

    Returns:
        The destination path as a string.

    Raises:
        FileNotFoundError: If the source file does not exist.
        OSError: If the file is inaccessible or locked.
    """
    ensure_directories()
    source = Path(filepath).resolve()

    if not source.is_file():
        raise FileNotFoundError(f"File not found: {filepath}")

    dest_dir = DELETED_DIR if DELETED_DIR.exists() else LEGACY_DELETED_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest = _unique_name(dest_dir, source.name)
    shutil.move(str(source), str(dest))
    return str(dest)


def move_to_museum(filepath: str) -> str:
    """
    Safely preserve an 'infected' file inside the threat_museum directory.

    SAFETY:
    - Does NOT execute or open the file.
    - Resolves collisions with unique numbered suffix.
    - Never overwrites existing museum files.

    Args:
        filepath: Path to the file to preserve.

    Returns:
        The destination path as a string.

    Raises:
        FileNotFoundError: If the source file does not exist.
        OSError: If the file is inaccessible or locked.
    """
    ensure_directories()
    source = Path(filepath).resolve()

    if not source.is_file():
        raise FileNotFoundError(f"File not found: {filepath}")

    dest_dir = MUSEUM_DIR if MUSEUM_DIR.exists() else LEGACY_MUSEUM_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest = _unique_name(dest_dir, source.name)
    # Copy the file into museum so it is preserved in both the original folder and museum vault
    shutil.copy2(str(source), str(dest))
    return str(dest)


def get_deleted_dir() -> Path:
    """Return the deleted_safe_files directory path."""
    return DELETED_DIR if DELETED_DIR.exists() else LEGACY_DELETED_DIR


def get_museum_dir() -> Path:
    """Return the threat_museum directory path."""
    return MUSEUM_DIR if MUSEUM_DIR.exists() else LEGACY_MUSEUM_DIR
