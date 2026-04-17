import sqlite3

DB_NAME = "goodreads.db"


def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS book_genres")
    cursor.execute("DROP TABLE IF EXISTS genres")
    cursor.execute("DROP TABLE IF EXISTS books")

    # Books table
    cursor.execute("""
    CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        rating REAL,
        published TEXT,
        pages INTEGER,
        url TEXT UNIQUE
    )
    """)

    # Genres table
    cursor.execute("""
    CREATE TABLE genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    # Junction table
    cursor.execute("""
    CREATE TABLE book_genres (
        book_id INTEGER,
        genre_id INTEGER,
        FOREIGN KEY(book_id) REFERENCES books(id),
        FOREIGN KEY(genre_id) REFERENCES genres(id)
    )
    """)

    conn.commit()
    conn.close()
