# This module handles all local database access for the app.
# SQLite is a good free-tier choice because it requires no separate database service.

import sqlite3
from pathlib import Path

from config import DATA_DIR, DB_PATH


def ensure_db() -> None:
    """Create the SQLite database and table if they do not already exist."""
    # Ensure the data folder exists before creating the database file.
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                base TEXT NOT NULL,
                target TEXT NOT NULL,
                rate REAL NOT NULL,
                fetched_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_exchange_rates_fetched_at ON exchange_rates(fetched_at)"
        )
        conn.commit()


def save_rate(base: str, target: str, rate: float, fetched_at: str) -> None:
    """Save one exchange-rate check into the local SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO exchange_rates (base, target, rate, fetched_at) VALUES (?, ?, ?, ?)",
            (base, target, rate, fetched_at),
        )
        conn.commit()


def get_latest_rate():
    """Return the most recent stored KES/TZS rate."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT base, target, rate, fetched_at FROM exchange_rates ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return dict(row) if row else None


def get_history(limit: int = 24):
    """Return the last N stored exchange-rate samples for graphing or display."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT base, target, rate, fetched_at
            FROM exchange_rates
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]
