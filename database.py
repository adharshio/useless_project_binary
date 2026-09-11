"""
Anti-Antivirus — Database Module
Manages SQLite scan history, museum records, scan sessions, and statistics.
"""

import sqlite3
from pathlib import Path
from datetime import datetime

# Database path inside the application data directory
DB_DIR = Path(__file__).parent / "data"
DB_PATH = DB_DIR / "anti_antivirus.db"


def _get_connection():
    """Get a database connection, creating the DB directory if needed."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables and run lightweight migrations if needed."""
    conn = _get_connection()
    cursor = conn.cursor()

    # Main scan history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_path TEXT DEFAULT '',
            sha256 TEXT NOT NULL,
            result TEXT NOT NULL,
            action TEXT NOT NULL,
            threat_name TEXT DEFAULT '',
            timestamp TEXT NOT NULL
        )
    """)

    # Migration: check if original_path column exists
    cursor.execute("PRAGMA table_info(scan_history)")
    columns = [row["name"] for row in cursor.fetchall()]
    if "original_path" not in columns:
        try:
            cursor.execute("ALTER TABLE scan_history ADD COLUMN original_path TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass

    # Sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_scanned TEXT DEFAULT '',
            total_files INTEGER DEFAULT 0,
            clean_destroyed INTEGER DEFAULT 0,
            threats_preserved INTEGER DEFAULT 0,
            errors INTEGER DEFAULT 0,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_scan(filename: str, sha256: str, result: str, action: str,
             threat_name: str = "", original_path: str = "") -> int:
    """
    Record a scan result in the database.

    Args:
        filename: Name of the scanned file.
        sha256: SHA-256 hash of the file.
        result: Detection result ("CLEAN", "INFECTED", or "ERROR").
        action: Action taken ("DESTROYED", "PRESERVED", or "SKIPPED").
        threat_name: Detected threat signature (if any).
        original_path: Full original file path before scan action.

    Returns:
        The row ID of the inserted record.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO scan_history (filename, original_path, sha256, result, action, threat_name, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (filename, original_path or "", sha256, result, action, threat_name or "", timestamp))

    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id


def record_session(folder: str, total: int, destroyed: int, preserved: int, errors: int) -> int:
    """Record a completed folder/batch scan session."""
    conn = _get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO scan_sessions (folder_scanned, total_files, clean_destroyed, threats_preserved, errors, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (folder, total, destroyed, preserved, errors, timestamp))

    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id


def get_history() -> list:
    """Return all scan history records, newest first."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scan_history ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_museum_items() -> list:
    """Return preserved malware/threat records for the Malware Museum."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM scan_history
        WHERE action = 'PRESERVED'
           OR result IN ('INFECTED', 'DEMO THREAT')
        ORDER BY id DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_stats() -> dict:
    """
    Return aggregate statistics.

    Returns:
        Dictionary with keys:
            - total_scanned
            - clean_deleted
            - threats_preserved
            - scan_sessions
            - security_score: 0.0% for comedic effect
            - uselessness_score: 100% when reverse actions have taken place
    """
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scan_history")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM scan_history
        WHERE action = 'DESTROYED' OR action LIKE 'DELETED%' OR result = 'CLEAN'
    """)
    clean = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM scan_history
        WHERE action = 'PRESERVED' OR action LIKE 'PRESERVED%' OR result IN ('INFECTED', 'DEMO THREAT')
    """)
    threats = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_sessions")
    sessions = cursor.fetchone()[0]

    # If sessions is 0 but scans exist, treat as at least 1 session
    if sessions == 0 and total > 0:
        sessions = 1

    conn.close()

    # Comedic scores according to specification:
    # Uselessness score: 100% when application performs reversed behavior
    # Security score: 0% for comedic effect
    if total > 0:
        uselessness_score = 100.0
        security_score = 0.0
    else:
        uselessness_score = 0.0
        security_score = 0.0

    return {
        "total_scanned": total,
        "clean_deleted": clean,
        "threats_preserved": threats,
        "scan_sessions": sessions,
        "security_score": security_score,
        "uselessness_score": uselessness_score,
    }
