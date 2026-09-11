"""
Anti-Antivirus — Demo Files Module
Generates harmless demo test files for demonstration purposes.
These files are simple .txt files with silly content — NO real malware.
"""

import os
from pathlib import Path
import hashlib

# Directory where demo sample files are stored
DEMO_DIR = Path(__file__).parent / "data" / "demo_samples"

# Demo file definitions: filename → content
DEMO_FILES = {
    "totally_not_a_virus.txt": (
        "THIS IS A DEMO FILE — NOT A REAL VIRUS\n"
        "=========================================\n"
        "If you're reading this, congratulations!\n"
        "You found the most dangerous text file ever created.\n"
        "It does absolutely nothing malicious.\n"
        "Threat Level: Imaginary\n"
    ),
    "malware_recipe.txt": (
        "THIS IS A DEMO FILE — NOT REAL MALWARE\n"
        "========================================\n"
        "Recipe for Digital Chaos:\n"
        "1. Open Notepad\n"
        "2. Type 'Hello World'\n"
        "3. Save file\n"
        "4. Panic\n"
        "Serves: 0 victims\n"
    ),
    "ransomware_but_polite.txt": (
        "THIS IS A DEMO FILE — NOT REAL RANSOMWARE\n"
        "============================================\n"
        "Dear User,\n"
        "We have encrypted your... just kidding.\n"
        "We would never do that. Have a nice day!\n"
        "Payment required: $0.00\n"
        "Sincerely, The Polite Hackers\n"
    ),
    "trojan_horse_toy.txt": (
        "THIS IS A DEMO FILE — NOT A REAL TROJAN\n"
        "==========================================\n"
        "I am a Trojan Horse.\n"
        "But I'm made of plastic and I'm 3 inches tall.\n"
        "I came free with a kids meal.\n"
        "Backdoor access: to the toy box\n"
    ),
    "spyware_diary.txt": (
        "THIS IS A DEMO FILE — NOT REAL SPYWARE\n"
        "=========================================\n"
        "Day 1: Watched the user type 'hello'.\n"
        "Day 2: User watched cat videos for 6 hours.\n"
        "Day 3: I'm starting to enjoy the cat videos too.\n"
        "Data exfiltrated: 0 bytes\n"
    ),
    "worm_but_cute.txt": (
        "THIS IS A DEMO FILE — NOT A REAL WORM\n"
        "========================================\n"
        "I'm a computer worm!\n"
        "I replicate by... well, I don't actually replicate.\n"
        "I'm more of a computer caterpillar, really.\n"
        "Systems infected: my own feelings\n"
    ),
}

# Threat names for display in the museum
THREAT_NAMES = {
    "totally_not_a_virus.txt": "GenericVirus.FakeAlert.A",
    "malware_recipe.txt": "Cookbook.Malware.Recipe.B",
    "ransomware_but_polite.txt": "Ransom.Polite.Kindware.C",
    "trojan_horse_toy.txt": "Trojan.PlasticHorse.Toy.D",
    "spyware_diary.txt": "Spyware.CatVideoWatcher.E",
    "worm_but_cute.txt": "Worm.Caterpillar.Cute.F",
}


def _compute_hash(content: str) -> str:
    """Compute SHA-256 hash of file content string."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def create_demo_files() -> dict:
    """
    Create all demo sample files and return a dict of hash → threat_name.

    Returns:
        Dictionary mapping SHA-256 hashes to threat display names.
    """
    DEMO_DIR.mkdir(parents=True, exist_ok=True)

    threat_hashes = {}

    for filename, content in DEMO_FILES.items():
        filepath = DEMO_DIR / filename
        # Always rewrite to ensure consistent hashes
        filepath.write_text(content, encoding="utf-8")

        file_hash = _compute_hash(content)
        threat_name = THREAT_NAMES.get(filename, "Unknown.Demo.Threat")
        threat_hashes[file_hash] = threat_name

    return threat_hashes


def get_demo_threat_hashes() -> dict:
    """
    Get the hash → threat_name mapping without creating files.
    Uses the known content to compute hashes deterministically.

    Returns:
        Dictionary mapping SHA-256 hashes to threat display names.
    """
    threat_hashes = {}
    for filename, content in DEMO_FILES.items():
        file_hash = _compute_hash(content)
        threat_name = THREAT_NAMES.get(filename, "Unknown.Demo.Threat")
        threat_hashes[file_hash] = threat_name
    return threat_hashes


def get_demo_dir() -> Path:
    """Return the path to the demo samples directory."""
    return DEMO_DIR
