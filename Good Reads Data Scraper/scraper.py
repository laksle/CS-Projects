
"""Automated Goodreads List web scraper using Selenium and BeautifulSoup that extracts book metadata and stores 
it in a SQLite database for analysis and visualization"""

import time
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from database import init_db, get_connection
import os


DB_NAME = "goodreads.db"

if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    print("Old database deleted")

init_db()
print("New database created")


def safe_text(el):
    try:
        return el.get_text(strip=True)
    except:
        return None

def safe_float(el):
    try:
        return float(el.get_text(strip=True))
    except:
        return None

conn = get_connection()
cursor = conn.cursor()


driver = webdriver.Chrome()
driver.set_window_position(-2000, 0)

list_url = "https://www.goodreads.com/list/show/161527.Best_Sci_fi_Fantasy_Short_Story_Collections"
driver.get(list_url)

time.sleep(3)
soup = BeautifulSoup(driver.page_source, "lxml")


book_links = set()

for a in soup.find_all("a", href=True):
    if "/book/show/" in a["href"]:
        book_links.add("https://www.goodreads.com" + a["href"].split("?")[0])

book_links = list(book_links)
print(f"Found {len(book_links)} books")

for i, url in enumerate(book_links[:10]):
    print(f"Scraping {i+1}/{len(book_links)}")

    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    title = safe_text(soup.find("h1"))
    author = safe_text(
        soup.find("h3", {"class": "Text Text__title3 Text__regular"})
    )

    rating = safe_float(
        soup.find(class_="RatingStatistics__rating")
    )

    page_count = None
    publish_date = None

    details = soup.find("div", class_="FeaturedDetails")

    if details:
        text_blocks = [t.get_text(" ", strip=True) for t in details.find_all("p")]

        for block in text_blocks:

            if "pages" in block.lower():
                match = re.search(r"(\d+)", block.replace(",", ""))
                if match:
                    page_count = int(match.group(1))

            elif any(m in block for m in [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]):
                publish_date = block


    # genres
    genre_tags = soup.find_all(class_="BookPageMetadataSection__genreButton")
    genres = list({g.get_text(strip=True) for g in genre_tags})
#Books Table Insert
    cursor.execute("""
        INSERT OR IGNORE INTO books
        (title, author, rating, published, pages, url)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
        title,
        author,
        rating,
        publish_date,
        page_count,
        url
    ))

    cursor.execute("SELECT id FROM books WHERE url = ?", (url,))
    book_id = cursor.fetchone()[0]


#Genres/Book_table Insert
    for g in genres:
        cursor.execute("""
           INSERT OR IGNORE INTO genres (name)
           VALUES (?)
           """, (g,))
        cursor.execute("SELECT id FROM genres WHERE name = ?", (g,))
        genre_id = cursor.fetchone()[0]

        cursor.execute("""
           INSERT OR IGNORE INTO book_genres (book_id, genre_id)
           VALUES (?, ?)
           """, (book_id, genre_id))
    conn.commit()


driver.quit()
conn.close()

print("\nScraping is finished. Data stored in SQLite DB.")
