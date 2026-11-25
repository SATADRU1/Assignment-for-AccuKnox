import sqlite3
import requests

API_URL = "https://openlibrary.org/search.json"
DB_FILE = "books.db"


def fetch_books(query="python", limit=20):
    params = {"q": query, "limit": limit,
              "fields": "title,author_name,first_publish_year"}
    resp = requests.get(API_URL, params=params, timeout=15)
    resp.raise_for_status()
    books = []
    for d in resp.json().get("docs", []):
        books.append((
            d.get("title", "Unknown"),
            ", ".join(d.get("author_name", ["Unknown"])),
            d.get("first_publish_year"),
        ))
    return books


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            publication_year INTEGER,
            UNIQUE(title, author)
        )""")


def save_books(conn, books):
    conn.executemany(
        "INSERT OR IGNORE INTO books (title, author, publication_year) VALUES (?, ?, ?)",
        books)
    conn.commit()


def display_books(conn):
    rows = conn.execute(
        "SELECT id, title, author, publication_year FROM books ORDER BY id").fetchall()
    print(f"{'ID':<4}{'Title':<45}{'Author':<30}{'Year':<6}")
    print("-" * 85)
    for r in rows:
        print(f"{r[0]:<4}{str(r[1])[:43]:<45}{str(r[2])[:28]:<30}{str(r[3] or ''):<6}")


if __name__ == "__main__":
    try:
        data = fetch_books()
    except requests.RequestException as e:
        raise SystemExit(f"API request failed: {e}")
    with sqlite3.connect(DB_FILE) as conn:
        init_db(conn)
        save_books(conn, data)
        display_books(conn)