import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "articles.db")


def create_articles_table():
    """Create the articles table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            content TEXT,
            summary TEXT,
            source_url TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def store_article(article_data: dict) -> bool:
    """Store an article. Returns True if stored, False if duplicate."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO articles (title, author, content, summary, source_url)
            VALUES (:title, :author, :content, :summary, :source_url)
        """, article_data)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def article_exists(source_url: str) -> bool:
    """Return True if an article with the given URL is already stored."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM articles WHERE source_url = ?", (source_url,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def get_all_summaries_data() -> list:
    """Return all articles as a list of dicts, newest first."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles ORDER BY created_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_article_by_id(article_id: int) -> dict | None:
    """Return a single article by ID, or None if not found."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_article_by_id(article_id: int) -> bool:
    """Delete a single article by ID. Returns True if deleted, False if not found."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted > 0


def clear_all_articles() -> int:
    """Delete all articles. Returns the number of rows deleted."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted
