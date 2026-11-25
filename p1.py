import sqlite3
import requests

# Primary API - Open Library (may sometimes timeout)
API_URL = "https://openlibrary.org/search.json"
DB_FILE = "books.db"

# Fallback sample data if API fails or returns empty
SAMPLE_BOOKS = [
    ("Learning Python", "Mark Lutz", 1999),
    ("Python For Data Analysis", "Wes McKinney", 2012),
    ("Fluent Python", "Luciano Ramalho", 2015),
    ("Python Cookbook", "Alex Martelli", 2002),
    ("Core Python Programming", "R. Nageswara Rao", 2016),
    ("Black Hat Python", "Justin Seitz", 2014),
    ("Automate the Boring Stuff with Python", "Al Sweigart", 2015),
    ("Python Crash Course", "Eric Matthes", 2019),
    ("Python for Everybody", "Charles Severance", 2016),
    ("Head First Python", "Paul Barry", 2010),
    ("Think Python", "Allen Downey", 2009),
    ("Effective Python", "Brett Slatkin", 2015),
]


def fetch_books():
    try:
        # Try OpenLibrary API
        params = {"q": "python", "limit": 20, "fields": "title,author_name,first_publish_year"}
        resp = requests.get(API_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json().get("docs", [])
        
        if not data:
            raise ValueError("No data from API")
        
        books = []
        for d in data:
            books.append((
                d.get("title", "Unknown"),
                ", ".join(d.get("author_name", ["Unknown"]))[:30],
                d.get("first_publish_year"),
            ))
        return books
    except Exception as e:
        print(f"API request failed ({type(e).__name__}). Using sample data.")
        return SAMPLE_BOOKS


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
    data = fetch_books()
    with sqlite3.connect(DB_FILE) as conn:
        init_db(conn)
        save_books(conn, data)
        display_books(conn)