"""
Windows De-fender — Scanner Module
Provides both hash-based demo scanning and ClamAV-based real scanning.

SAFETY:
- Scanner NEVER moves, deletes, or executes any file.
- Scanner only reads files to compute hashes and runs clamscan externally.
- ClamAV's clamscan.exe only reads files — it does not modify them.
"""

import hashlib
import subprocess
import os
from pathlib import Path
from demo_files import get_demo_threat_hashes


# ── Directories to skip during recursive discovery ──
SKIP_DIRS = {
    "__pycache__", ".git", ".venv", "venv", "node_modules",
    "Deleted_Safe_Files", "Threat_Museum", "deleted_safe_files",
    "threat_museum", ".mypy_cache", ".pytest_cache",
}

# ── System directories that must NEVER be selected for scanning ──
BLOCKED_DIRS = {
    os.path.normcase(p) for p in [
        "C:\\Windows", "C:\\Windows\\System32", "C:\\Windows\\SysWOW64",
        "C:\\Program Files", "C:\\Program Files (x86)",
        "C:\\ProgramData", "C:\\Recovery", "C:\\$Recycle.Bin",
        "C:\\System Volume Information",
    ]
}


def compute_sha256(filepath: str) -> str:
    """
    Compute the SHA-256 hash of a file.

    Args:
        filepath: Path to the file to hash.

    Returns:
        Hex string of the SHA-256 hash.
    """
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


# ─────────────────────────────────────────────
# Hash-based demo scanning (original behavior)
# ─────────────────────────────────────────────

def scan_file(filepath: str) -> dict:
    """
    Scan a file by computing its hash and checking against demo threats.
    Original hash-based detection — kept for backward compatibility.

    Args:
        filepath: Path to the file to scan.

    Returns:
        Dictionary with keys:
            - filename: basename of the file
            - filepath: full path
            - sha256: hex hash string
            - result: "CLEAN" or "DEMO THREAT"
            - threat_name: name of the demo threat (empty if clean)
    """
    filepath = str(filepath)
    file_hash = compute_sha256(filepath)
    threat_hashes = get_demo_threat_hashes()

    if file_hash in threat_hashes:
        return {
            "filename": Path(filepath).name,
            "filepath": filepath,
            "sha256": file_hash,
            "result": "DEMO THREAT",
            "threat_name": threat_hashes[file_hash],
        }
    else:
        return {
            "filename": Path(filepath).name,
            "filepath": filepath,
            "sha256": file_hash,
            "result": "CLEAN",
            "threat_name": "",
        }


# ─────────────────────────────────────────────
# ClamAV-based scanning
# ─────────────────────────────────────────────

def find_clamscan() -> str | None:
    """
    Search for clamscan.exe in common installation paths.

    Returns:
        Full path to clamscan.exe, or None if not found.
    """
    search_paths = [
        r"C:\Program Files\ClamAV\clamscan.exe",
        r"C:\Program Files (x86)\ClamAV\clamscan.exe",
        r"C:\ClamAV\clamscan.exe",
    ]

    # Check PATH first
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        candidate = os.path.join(path_dir, "clamscan.exe")
        if os.path.isfile(candidate):
            return candidate

    # Check known locations
    for path in search_paths:
        if os.path.isfile(path):
            return path

    return None


def scan_file_clamav(filepath: str, clamscan_path: str = None) -> dict:
    """
    Scan a single file using ClamAV's clamscan.exe.

    This function ONLY reads the file — it does NOT move, delete, or execute it.

    Args:
        filepath: Path to the file to scan.
        clamscan_path: Optional explicit path to clamscan.exe.

    Returns:
        Dictionary with keys:
            - filename: basename of the file
            - filepath: full path
            - sha256: hex hash string
            - result: "CLEAN", "INFECTED", or "ERROR"
            - threat_name: name of the detected threat (empty if clean)
    """
    filepath = str(filepath)
    filename = Path(filepath).name

    # Compute SHA-256 first
    try:
        file_hash = compute_sha256(filepath)
    except (PermissionError, OSError) as e:
        return {
            "filename": filename,
            "filepath": filepath,
            "sha256": "",
            "result": "ERROR",
            "threat_name": f"Hash error: {e}",
        }

    # Find clamscan
    if clamscan_path is None:
        clamscan_path = find_clamscan()

    if clamscan_path is None:
        # Fallback to hash-based demo scan if ClamAV not installed
        return scan_file(filepath)

    # Run clamscan — NEVER executes the target file
    try:
        result = subprocess.run(
            [clamscan_path, "--no-summary", "--stdout", filepath],
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout per file
        )

        # Parse clamscan output
        # Format: "/path/to/file: OK" or "/path/to/file: ThreatName FOUND"
        stdout = result.stdout.strip()

        if result.returncode == 0:
            # Clean file
            return {
                "filename": filename,
                "filepath": filepath,
                "sha256": file_hash,
                "result": "CLEAN",
                "threat_name": "",
            }
        elif result.returncode == 1:
            # Infected file — parse threat name
            threat_name = "Unknown Threat"
            if "FOUND" in stdout:
                # Extract threat name from "filepath: ThreatName FOUND"
                parts = stdout.rsplit(":", 1)
                if len(parts) == 2:
                    threat_part = parts[1].strip()
                    if threat_part.endswith("FOUND"):
                        threat_name = threat_part[:-5].strip()

            return {
                "filename": filename,
                "filepath": filepath,
                "sha256": file_hash,
                "result": "INFECTED",
                "threat_name": threat_name,
            }
        else:
            # Error (returncode 2 = error in clamscan)
            error_msg = result.stderr.strip() or result.stdout.strip() or "Unknown error"
            return {
                "filename": filename,
                "filepath": filepath,
                "sha256": file_hash,
                "result": "ERROR",
                "threat_name": f"Scan error: {error_msg[:100]}",
            }

    except subprocess.TimeoutExpired:
        return {
            "filename": filename,
            "filepath": filepath,
            "sha256": file_hash,
            "result": "ERROR",
            "threat_name": "Scan timed out (60s)",
        }
    except Exception as e:
        return {
            "filename": filename,
            "filepath": filepath,
            "sha256": file_hash,
            "result": "ERROR",
            "threat_name": f"Scan error: {str(e)[:100]}",
        }


# ─────────────────────────────────────────────
# Recursive file discovery
# ─────────────────────────────────────────────

def discover_files(folder_path: str) -> list:
    """
    Recursively discover all files inside the selected folder.

    Safety:
    - Skips directories in SKIP_DIRS (e.g. __pycache__, .git).
    - Does NOT follow symbolic links outside the selected folder.
    - Catches and skips PermissionError / inaccessible files.

    Args:
        folder_path: Absolute path to the folder to scan.

    Returns:
        Sorted list of absolute file paths (strings).
    """
    folder = Path(folder_path).resolve()
    files = []

    try:
        for entry in sorted(folder.rglob("*")):
            # Skip directories themselves — we only want files
            if entry.is_dir():
                continue

            # Skip if any parent directory is in SKIP_DIRS
            rel_parts = entry.relative_to(folder).parts
            if any(part in SKIP_DIRS for part in rel_parts):
                continue

            # Do not follow symlinks that point outside the selected folder
            if entry.is_symlink():
                try:
                    resolved = entry.resolve()
                    if not str(resolved).startswith(str(folder)):
                        continue
                except (OSError, ValueError):
                    continue

            # Verify file is accessible
            try:
                if entry.is_file():
                    files.append(str(entry))
            except (PermissionError, OSError):
                continue

    except PermissionError:
        pass  # Top-level permission error — return what we have

    return files


def is_blocked_directory(folder_path: str) -> bool:
    """
    Check if a directory is a system/protected directory that should not be scanned.

    Args:
        folder_path: Path to check.

    Returns:
        True if the directory is blocked, False otherwise.
    """
    normalized = os.path.normcase(os.path.abspath(folder_path))

    # Check exact match
    if normalized in BLOCKED_DIRS:
        return True

    # Check if it's a root drive (e.g., "C:\")
    if len(normalized) <= 3 and normalized.endswith(("\\", ":")):
        return True

    return False
