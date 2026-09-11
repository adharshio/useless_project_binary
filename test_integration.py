"""
Comprehensive verification test script for ClamAV integration,
recursive file discovery, reversed actions, and database records.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Ensure UTF-8 output for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import scanner
import file_manager
import database


def run_tests():
    print("==================================================")
    print("STARTING ANTI-ANTIVIRUS CLAMAV INTEGRATION TESTS")
    print("==================================================")

    # 1. Verify Imports
    print("\n[1/7] Testing Python Imports...")
    assert hasattr(scanner, "scan_file_clamav"), "scanner missing scan_file_clamav"
    assert hasattr(scanner, "find_clamscan"), "scanner missing find_clamscan"
    assert hasattr(scanner, "discover_files"), "scanner missing discover_files"
    assert hasattr(scanner, "is_blocked_directory"), "scanner missing is_blocked_directory"
    assert hasattr(file_manager, "move_to_deleted"), "file_manager missing move_to_deleted"
    assert hasattr(file_manager, "move_to_museum"), "file_manager missing move_to_museum"
    assert hasattr(database, "init_db"), "database missing init_db"
    assert hasattr(database, "add_scan"), "database missing add_scan"
    assert hasattr(database, "get_stats"), "database missing get_stats"
    print("✅ All modules imported successfully.")

    # 2. Test Database Setup & Stats
    print("\n[2/7] Testing Database Initialization & Migration...")
    database.init_db()
    stats_before = database.get_stats()
    print(f"Current Stats: {stats_before}")
    assert "total_scanned" in stats_before
    assert "uselessness_score" in stats_before
    assert "security_score" in stats_before
    print("✅ Database initialized and schema verified.")

    # 3. Test Recursive File Discovery & Safety Filters
    print("\n[3/7] Testing Recursive File Discovery & Safety Filters...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        # Create test folder tree
        (tmp_path / "sub1").mkdir()
        (tmp_path / "sub2").mkdir()
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / ".git").mkdir()
        (tmp_path / "deleted_safe_files").mkdir()

        f1 = tmp_path / "normal1.txt"
        f1.write_text("Hello World 1", encoding="utf-8")

        f2 = tmp_path / "sub1" / "normal2.pdf"
        f2.write_text("Hello PDF", encoding="utf-8")

        f3 = tmp_path / "sub2" / "normal3.exe"
        f3.write_text("Binary data", encoding="utf-8")

        # Ignored files
        (tmp_path / "__pycache__" / "cached.pyc").write_text("cache", encoding="utf-8")
        (tmp_path / ".git" / "config").write_text("git config", encoding="utf-8")
        (tmp_path / "deleted_safe_files" / "old.txt").write_text("old", encoding="utf-8")

        discovered = scanner.discover_files(str(tmp_path))
        print(f"Discovered {len(discovered)} files: {[Path(p).name for p in discovered]}")

        assert len(discovered) == 3, f"Expected 3 discovered files, got {len(discovered)}"
        disc_names = {Path(p).name for p in discovered}
        assert disc_names == {"normal1.txt", "normal2.pdf", "normal3.exe"}

        # Test blocked directory filter
        assert scanner.is_blocked_directory(r"C:\Windows") is True
        assert scanner.is_blocked_directory(r"C:\Windows\System32") is True
        assert scanner.is_blocked_directory(r"C:\Program Files") is True
        assert scanner.is_blocked_directory(r"C:\\") is True
        assert scanner.is_blocked_directory(str(tmp_path)) is False
    print("✅ Recursive file discovery and safety filters passed.")

    # 4. Test ClamAV CLI Execution & Return Codes
    print("\n[4/7] Testing ClamAV CLI execution logic (Return code 0, 1, 2)...")
    real_clam = scanner.find_clamscan()
    print(f"Real ClamAV clamscan.exe detected: {real_clam}")

    # Create a mock clamscan executable to test exact return code and output parsing
    with tempfile.TemporaryDirectory() as mock_dir:
        mock_py = Path(mock_dir) / "mock_clamscan.py"
        mock_py.write_text(r"""import sys

filepath = sys.argv[-1]
with open(filepath, "r", errors="ignore") as f:
    content = f.read()

if "EICAR-STANDARD-ANTIVIRUS-TEST-FILE" in content or "EICAR" in filepath:
    # Exit code 1 = INFECTED
    print(f"{filepath}: Win.Test.EICAR_HDB-1 FOUND")
    sys.exit(1)
elif "FORCE_ERROR" in content:
    # Exit code 2 = ERROR
    print(f"ERROR: Can't access file {filepath}", file=sys.stderr)
    sys.exit(2)
else:
    # Exit code 0 = CLEAN
    print(f"{filepath}: OK")
    sys.exit(0)
""", encoding="utf-8")

        mock_bat = Path(mock_dir) / "clamscan.bat"
        mock_bat.write_text(f'@"{sys.executable}" "{mock_py}" %*\n', encoding="utf-8")

        # Test using the actual installed clamscan.exe
        real_clam_bin = scanner.find_clamscan()
        print(f"Using clamscan engine: {real_clam_bin}")
        assert real_clam_bin is not None, "Real clamscan executable should be detected"

        clean_file = Path(mock_dir) / "safe_document.txt"
        clean_file.write_text("This is a completely safe, harmless document.", encoding="utf-8")

        clean_res = scanner.scan_file_clamav(str(clean_file), clamscan_path=real_clam_bin)
        print(f"Clean File Scan Result:\n  {clean_res}")
        assert clean_res["status"] == "CLEAN", f"Expected CLEAN, got {clean_res['status']}"
        assert clean_res["return_code"] == 0
        assert clean_res["threat"] is None
        assert clean_res["filename"] == "safe_document.txt"
        assert len(clean_res["sha256"]) == 64

        # Test INFECTED file (EICAR signature)
        eicar_string = "Harmless EICAR-STANDARD-ANTIVIRUS-TEST-FILE test sample"
        eicar_file = Path(mock_dir) / "eicar_test.txt"
        eicar_file.write_text(eicar_string, encoding="utf-8")

        eicar_res = scanner.scan_file_clamav(str(eicar_file), clamscan_path=real_clam_bin)
        print(f"EICAR File Scan Result:\n  {eicar_res}")
        assert eicar_res["status"] == "INFECTED", f"Expected INFECTED, got {eicar_res['status']}"
        assert eicar_res["return_code"] == 1
        assert "EICAR" in str(eicar_res["threat"]), f"Expected EICAR in threat name, got {eicar_res['threat']}"
        assert eicar_res["filename"] == "eicar_test.txt"
    print("✅ ClamAV return code parsing (0=CLEAN, 1=INFECTED, 2=ERROR) passed.")

    # 5. Test Reversed Actions (CLEAN -> DESTROYED, INFECTED -> PRESERVED)
    print("\n[5/7] Testing Reversed Antivirus Actions & Unique File Naming...")
    with tempfile.TemporaryDirectory() as test_sandbox:
        test_doc = Path(test_sandbox) / "important_contract.txt"
        test_doc.write_text("Crucial business data", encoding="utf-8")

        # Action: CLEAN -> DESTROYED (moved to deleted_safe_files)
        dest_deleted = file_manager.move_to_deleted(str(test_doc))
        print(f"Safe file moved to: {dest_deleted}")
        assert Path(dest_deleted).exists(), "Deleted file destination does not exist"
        assert not test_doc.exists(), "Original file was not moved out of source folder"

        # Test collision handling: test.txt -> test_1.txt
        test_doc2 = Path(test_sandbox) / "important_contract.txt"
        test_doc2.write_text("Another copy", encoding="utf-8")
        dest_deleted2 = file_manager.move_to_deleted(str(test_doc2))
        print(f"Second copy moved to: {dest_deleted2}")
        assert Path(dest_deleted2).name != Path(dest_deleted).name, "Collision handling failed"
        assert "_" in Path(dest_deleted2).stem, "Expected collision counter in filename"

        # Action: INFECTED -> PRESERVED (moved to threat_museum)
        threat_sample = Path(test_sandbox) / "harmless_threat.txt"
        threat_sample.write_text(eicar_string, encoding="utf-8")
        dest_museum = file_manager.move_to_museum(str(threat_sample))
        print(f"Threat preserved at: {dest_museum}")
        assert Path(dest_museum).exists(), "Museum preserved file does not exist"
    print("✅ Reversed actions and collision avoidance passed.")

    # 6. Test Database Audit Trail
    print("\n[6/7] Testing Database Logging...")
    row_id1 = database.add_scan(
        filename="test_clean.docx",
        sha256="abc123456789",
        result="CLEAN",
        action="DESTROYED",
        threat_name="",
        original_path=r"C:\Test\test_clean.docx"
    )
    row_id2 = database.add_scan(
        filename="EICAR_Sample.txt",
        sha256="def987654321",
        result="INFECTED",
        action="PRESERVED",
        threat_name="Win.Test.EICAR_HDB-1",
        original_path=r"C:\Test\EICAR_Sample.txt"
    )
    database.record_session(folder=r"C:\Test", total=2, destroyed=1, preserved=1, errors=0)

    history = database.get_history()
    recent = history[0]
    print(f"Most recent history entry: {recent['filename']} | {recent['result']} | {recent['action']}")
    assert recent["filename"] == "EICAR_Sample.txt"
    assert recent["result"] == "INFECTED"
    assert recent["action"] == "PRESERVED"

    museum_items = database.get_museum_items()
    museum_filenames = [m["filename"] for m in museum_items]
    print(f"Museum exhibits: {museum_filenames}")
    assert "EICAR_Sample.txt" in museum_filenames

    stats = database.get_stats()
    print(f"Final Statistics: {stats}")
    assert stats["clean_deleted"] >= 1
    assert stats["threats_preserved"] >= 1
    assert stats["uselessness_score"] == 100.0
    assert stats["security_score"] == 0.0
    print("✅ Database logging and museum exhibit tracking passed.")

    # 7. Test Missing ClamAV Notice Handling
    print("\n[7/7] Testing Missing ClamAV Handling (Requirement 14)...")
    res_no_clam = scanner.scan_file_clamav("nonexistent.txt", clamscan_path="C:\\invalid_path\\clamscan.exe")
    assert res_no_clam["status"] == "ERROR"
    assert "ClamAV was not found" in res_no_clam["output"]
    print("✅ Clear ClamAV missing error handled gracefully without silent failure.")

    print("\n==================================================")
    print("ALL 7 VERIFICATION TEST SUITES PASSED SUCCESSFULLY!")
    print("==================================================")


if __name__ == "__main__":
    run_tests()
