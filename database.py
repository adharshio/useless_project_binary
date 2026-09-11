"""
Anti-Antivirus — Database Module
Manages SQLite scan history, museum records, and statistics.
"""

import sqlite3
import os
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
    """Initialize the database and create tables if they don't exist."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            result TEXT NOT NULL,
            action TEXT NOT NULL,
            threat_name TEXT DEFAULT '',
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_scan(filename: str, sha256: str, result: str, action: str,
             threat_name: str = "") -> int:
    """
    Record a scan result in the database.

    Args:
        filename: Name of the scanned file.
        sha256: SHA-256 hash of the file.
        result: Detection result ("CLEAN" or "DEMO THREAT").
        action: Action taken ("DELETED" or "PRESERVED").
        threat_name: Name of the detected demo threat (if any).

    Returns:
        The row ID of the inserted record.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO scan_history (filename, sha256, result, action, threat_name, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (filename, sha256, result, action, threat_name, timestamp))

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
    """Return only preserved demo threat records for the Malware Museum."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM scan_history
        WHERE result = 'DEMO THREAT'
        ORDER BY id DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_stats() -> dict:
    """
    Return aggregate statistics.

    Returns:
        Dictionary with keys: total_scanned, clean_deleted, threats_preserved,
        security_score, uselessness_score.
    """
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scan_history")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE result = 'CLEAN'")
    clean = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE result = 'DEMO THREAT'")
    threats = cursor.fetchone()[0]

    conn.close()

    # Security score: intentionally terrible (lower is "better" for us)
    if total > 0:
        security_score = round(max(1, min(5, (threats / total) * 5 + 1)), 1)
        uselessness_score = round(min(99.9, 95 + (total * 0.3)), 1)
    else:
        security_score = 0.0
        uselessness_score = 0.0

    return {
        "total_scanned": total,
        "clean_deleted": clean,
        "threats_preserved": threats,
        "security_score": security_score,
        "uselessness_score": uselessness_score,
    }
