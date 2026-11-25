import csv
import sqlite3

CSV_FILE = "users.csv"
DB_FILE = "users.db"


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )""")


def import_csv(conn, path):
    inserted = skipped = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = (row.get("name") or "").strip()
            email = (row.get("email") or "").strip().lower()
            if not name or "@" not in email:
                skipped += 1
                continue
            cur = conn.execute(
                "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", (name, email))
            inserted += cur.rowcount
            skipped += 1 - cur.rowcount
    conn.commit()
    return inserted, skipped


if __name__ == "__main__":
    with sqlite3.connect(DB_FILE) as conn:
        init_db(conn)
        ins, skp = import_csv(conn, CSV_FILE)
        print(f"Inserted: {ins}, skipped (invalid/duplicate): {skp}")
        for row in conn.execute("SELECT * FROM users"):
            print(row)