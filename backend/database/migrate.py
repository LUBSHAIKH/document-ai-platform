"""Add missing columns to the documents table."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "documents.db"

MIGRATIONS = [
    ("indexed",         "ALTER TABLE documents ADD COLUMN indexed BOOLEAN DEFAULT 0"),
    ("indexed_at",      "ALTER TABLE documents ADD COLUMN indexed_at DATETIME"),
    ("embedding_chunks","ALTER TABLE documents ADD COLUMN embedding_chunks INTEGER DEFAULT 0"),
]

def run():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(documents)")
    existing = {row[1] for row in cur.fetchall()}

    for col, sql in MIGRATIONS:
        if col not in existing:
            print(f"Adding column: {col}")
            cur.execute(sql)
        else:
            print(f"Column already exists: {col}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    run()
