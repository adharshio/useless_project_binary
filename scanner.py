"""
Anti-Antivirus — Scanner Module
Computes file hashes and checks against demo threat database.
NO real malware scanning — purely hash-based demo detection.
"""

import hashlib
from pathlib import Path
from demo_files import get_demo_threat_hashes


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


def scan_file(filepath: str) -> dict:
    """
    Scan a file by computing its hash and checking against demo threats.

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
