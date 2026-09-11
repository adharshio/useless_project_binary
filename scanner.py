"""
Anti-Antivirus — Scanner Module
Provides ClamAV-based real scanning (clamscan.exe) with structured results,
recursive directory discovery, and safety filters.

SAFETY:
- Scanner NEVER moves, deletes, or executes any file.
- Scanner only reads files to compute hashes and passes paths to clamscan externally.
- ClamAV's clamscan.exe only reads files — it does not modify or execute them.
- Protected system directories are shielded from scanning.
"""

import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from demo_files import get_demo_threat_hashes


# ── Configurable ClamAV path ──
CLAMAV_PATH = os.environ.get("CLAMAV_PATH", None)
CLAMAV_DB_DIR = Path(__file__).parent / "data" / "clamav_db"


def set_clamscan_path(path: str | None):
    """Set custom path to clamscan.exe."""
    global CLAMAV_PATH
    CLAMAV_PATH = path


def get_clamscan_path() -> str | None:
    """Get current custom path to clamscan.exe."""
    return CLAMAV_PATH


def ensure_clamav_database() -> str:
    """
    Ensure local ClamAV signatures exist so clamscan works even before freshclam runs.
    Includes EICAR test string signature and demo threat patterns.
    """
    CLAMAV_DB_DIR.mkdir(parents=True, exist_ok=True)
    sig_file = CLAMAV_DB_DIR / "test_threats.ndb"
    if not sig_file.exists() or sig_file.stat().st_size == 0:
        # ClamAV .ndb format: ThreatName:TargetType:Offset:HexPattern
        # Hex for "EICAR-STANDARD-ANTIVIRUS-TEST-FILE"
        eicar_hex = "45494341522d5354414e444152442d414e544956495255532d544553542d46494c45"
        sig_file.write_text(f"Win.Test.EICAR_HDB-1:0:*:{eicar_hex}\n", encoding="utf-8")

    return str(CLAMAV_DB_DIR)


# ── Directories to skip during recursive discovery ──
SKIP_DIR_NAMES = {
    "__pycache__", ".git", ".venv", "venv", "node_modules",
    "deleted_safe_files", "threat_museum", ".mypy_cache", ".pytest_cache",
    "clamav_db",
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
    Safely compute the SHA-256 hash of a file.

    Args:
        filepath: Path to the file to hash.

    Returns:
        Hex string of the SHA-256 hash, or empty string on error.
    """
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return ""


# ─────────────────────────────────────────────
# ClamAV Locator & Status
# ─────────────────────────────────────────────

def find_clamscan(custom_path: str = None) -> str | None:
    """
    Locate clamscan.exe automatically in PATH, custom setting, or common locations.

    Returns:
        Full path to clamscan.exe if found, else None.
    """
    # 1. Custom explicit path argument
    if custom_path:
        return custom_path if os.path.isfile(custom_path) else None

    # 2. Configured CLAMAV_PATH variable
    if CLAMAV_PATH:
        if os.path.isfile(CLAMAV_PATH):
            return CLAMAV_PATH

    # 3. Check system PATH
    which_bin = shutil.which("clamscan") or shutil.which("clamscan.exe")
    if which_bin and os.path.isfile(which_bin):
        return which_bin

    # 4. Common Windows installation locations
    candidate_paths = [
        r"C:\Program Files\ClamAV\clamscan.exe",
        r"C:\Program Files (x86)\ClamAV\clamscan.exe",
        r"C:\ClamAV\clamscan.exe",
        r"C:\Program Files\ClamAV\bin\clamscan.exe",
        r"C:\ClamAV\bin\clamscan.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\ClamAV\clamscan.exe"),
        os.path.expandvars(r"%ProgramW6432%\ClamAV\clamscan.exe"),
    ]

    for path in candidate_paths:
        if os.path.isfile(path):
            return path

    return None


def is_clamav_available(custom_path: str = None) -> bool:
    """Check if ClamAV clamscan.exe is available."""
    return find_clamscan(custom_path) is not None


# ─────────────────────────────────────────────
# Structured ClamAV Scanner
# ─────────────────────────────────────────────

def scan_file_clamav(filepath: str, clamscan_path: str = None) -> dict:
    """
    Scan a single file using ClamAV's command-line scanner (clamscan.exe).

    SAFETY:
    - This function ONLY detects and returns results.
    - NEVER deletes, moves, executes, or modifies any file.
    - Uses subprocess safely without shell=True.

    ClamAV Return Codes:
        0 = CLEAN
        1 = INFECTED
        2 = ERROR

    Returns:
        Structured dictionary:
            - filename: basename
            - path: absolute full path
            - sha256: SHA-256 hash string
            - status: "CLEAN", "INFECTED", or "ERROR"
            - threat: threat name string if infected, else None
            - output: ClamAV output message
            - return_code: ClamAV exit code (int or None)
    """
    filepath = str(os.path.abspath(filepath))
    filename = Path(filepath).name

    # 1. Safely compute SHA-256 hash
    file_hash = compute_sha256(filepath)

    # 2. Locate clamscan.exe
    scanner_bin = find_clamscan(clamscan_path)
    if not scanner_bin:
        return {
            "filename": filename,
            "path": filepath,
            "sha256": file_hash,
            "status": "ERROR",
            "threat": None,
            "output": "ClamAV was not found. Please install ClamAV and make sure clamscan.exe is available, or configure CLAMAV_PATH.",
            "return_code": None,
        }

    # 3. Assemble command with database fallback if needed
    cmd = [scanner_bin, "--no-summary", "--stdout"]

    # If clamscan doesn't have system database directory, pass local db directory
    bin_parent = Path(scanner_bin).parent
    system_db = bin_parent / "database"
    if not system_db.exists() or not any(system_db.iterdir()):
        local_db = ensure_clamav_database()
        cmd.extend(["-d", local_db])

    cmd.append(filepath)

    # 4. Execute clamscan securely
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            shell=False,
        )

        stdout = proc.stdout.strip() if proc.stdout else ""
        stderr = proc.stderr.strip() if proc.stderr else ""
        combined_output = f"{stdout}\n{stderr}".strip() if stderr else stdout
        return_code = proc.returncode

        if return_code == 0:
            # CLEAN
            return {
                "filename": filename,
                "path": filepath,
                "sha256": file_hash,
                "status": "CLEAN",
                "threat": None,
                "output": stdout or "OK",
                "return_code": 0,
            }
        elif return_code == 1:
            # INFECTED: parse threat name from output
            # Output format: "<path>: <threat_name> FOUND"
            threat_name = "Detected Threat"
            for line in stdout.splitlines():
                if "FOUND" in line:
                    parts = line.rsplit(":", 1)
                    if len(parts) >= 2:
                        raw = parts[1].strip()
                        if raw.endswith("FOUND"):
                            threat_name = raw[:-5].strip()
                        else:
                            threat_name = raw
                        break

            return {
                "filename": filename,
                "path": filepath,
                "sha256": file_hash,
                "status": "INFECTED",
                "threat": threat_name,
                "output": stdout,
                "return_code": 1,
            }
        elif return_code == 2:
            # ERROR
            return {
                "filename": filename,
                "path": filepath,
                "sha256": file_hash,
                "status": "ERROR",
                "threat": None,
                "output": combined_output or "ClamAV scan error (return code 2)",
                "return_code": 2,
            }
        else:
            # Unexpected return code
            return {
                "filename": filename,
                "path": filepath,
                "sha256": file_hash,
                "status": "ERROR",
                "threat": None,
                "output": combined_output or f"ClamAV scan exited with code {return_code}",
                "return_code": return_code,
            }

    except subprocess.TimeoutExpired:
        return {
            "filename": filename,
            "path": filepath,
            "sha256": file_hash,
            "status": "ERROR",
            "threat": None,
            "output": "ClamAV scan timed out (60s limit reached)",
            "return_code": None,
        }
    except Exception as e:
        return {
            "filename": filename,
            "path": filepath,
            "sha256": file_hash,
            "status": "ERROR",
            "threat": None,
            "output": f"ClamAV execution failed: {e}",
            "return_code": None,
        }


# ─────────────────────────────────────────────
# Fallback / Unified Scan
# ─────────────────────────────────────────────

def scan_file(filepath: str, clamscan_path: str = None) -> dict:
    """
    Main scan entry point. Uses ClamAV if available, otherwise falls back to
    built-in demo threat hash checking for harmless testing.

    Returns structured dict matching Requirement 2 format.
    """
    filepath = str(os.path.abspath(filepath))
    filename = Path(filepath).name

    # Check if ClamAV is installed
    clam_bin = find_clamscan(clamscan_path)
    if clam_bin:
        res = scan_file_clamav(filepath, clamscan_path=clam_bin)
        # Add backward-compatible keys for existing callers if any
        res["result"] = res["status"]
        res["threat_name"] = res["threat"] or ""
        res["filepath"] = res["path"]
        return res

    # ClamAV not installed: check built-in demo hash catalog as fallback
    file_hash = compute_sha256(filepath)
    if not file_hash:
        return {
            "filename": filename,
            "path": filepath,
            "filepath": filepath,
            "sha256": "",
            "status": "ERROR",
            "result": "ERROR",
            "threat": None,
            "threat_name": "",
            "output": "Could not compute hash for file",
            "return_code": None,
        }

    threat_hashes = get_demo_threat_hashes()
    if file_hash in threat_hashes:
        threat_name = threat_hashes[file_hash]
        return {
            "filename": filename,
            "path": filepath,
            "filepath": filepath,
            "sha256": file_hash,
            "status": "INFECTED",
            "result": "INFECTED",
            "threat": threat_name,
            "threat_name": threat_name,
            "output": f"Demo Threat signature matched: {threat_name}",
            "return_code": 1,
        }
    else:
        return {
            "filename": filename,
            "path": filepath,
            "filepath": filepath,
            "sha256": file_hash,
            "status": "CLEAN",
            "result": "CLEAN",
            "threat": None,
            "threat_name": "",
            "output": "No demo threat signature detected",
            "return_code": 0,
        }


# ─────────────────────────────────────────────
# Recursive Directory Discovery & Safety
# ─────────────────────────────────────────────

def discover_files(folder_path: str) -> list[str]:
    """
    Recursively discover all files inside the selected folder.

    Safety:
    - Skips directories in SKIP_DIR_NAMES (case-insensitive).
    - Does NOT follow symbolic links outside the selected folder.
    - Catches and skips PermissionError / inaccessible files without crashing.

    Args:
        folder_path: Absolute path to the folder to scan.

    Returns:
        Sorted list of absolute file paths (strings).
    """
    folder = Path(folder_path).resolve()
    files = []

    try:
        for entry in sorted(folder.rglob("*")):
            # Skip directories themselves — we only collect files
            if entry.is_dir():
                continue

            # Skip if any parent directory is in skip list (case-insensitive)
            try:
                rel_parts = entry.relative_to(folder).parts
                if any(part.lower() in SKIP_DIR_NAMES for part in rel_parts):
                    continue
            except ValueError:
                continue

            # Do not follow symlinks pointing outside the selected folder
            if entry.is_symlink():
                try:
                    resolved = entry.resolve()
                    if not str(resolved).lower().startswith(str(folder).lower()):
                        continue
                except (OSError, ValueError):
                    continue

            # Verify file is accessible and normal file
            try:
                if entry.is_file():
                    files.append(str(entry.resolve()))
            except (PermissionError, OSError):
                continue

    except (PermissionError, OSError):
        pass  # Handle top-level permission error gracefully

    return files


def is_blocked_directory(folder_path: str) -> bool:
    """
    Check if a directory is a protected system directory that should not be scanned.

    Args:
        folder_path: Path to check.

    Returns:
        True if the directory is blocked, False otherwise.
    """
    try:
        normalized = os.path.normcase(os.path.abspath(folder_path))
    except Exception:
        return True

    # Check exact match or subdirectories of blocked dirs
    for b in BLOCKED_DIRS:
        if normalized == b or normalized.startswith(b + os.sep):
            return True

    # Check if it is a root drive (e.g. "C:\")
    if len(normalized) <= 3 and (normalized.endswith("\\") or normalized.endswith(":")):
        return True

    return False
