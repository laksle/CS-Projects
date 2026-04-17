#Run this file to generate charts for the data
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("goodreads.db")
cursor = conn.cursor()

#Top Rated Books

cursor.execute("""
SELECT title, rating
FROM books
WHERE rating IS NOT NULL
ORDER BY rating DESC
LIMIT 10
""")

top_books = cursor.fetchall()
titles = [x[0][:15] for x in top_books]
ratings = [x[1] for x in top_books]



# Top Genres
cursor.execute("""
SELECT g.name, COUNT(*) as count
FROM genres g
JOIN book_genres bg ON g.id = bg.genre_id
GROUP BY g.name
ORDER BY count DESC
LIMIT 10
""")

genre_data = cursor.fetchall()
genre_labels = [x[0] for x in genre_data]
genre_values = [x[1] for x in genre_data]



# Page Distribution

cursor.execute("""
SELECT pages
FROM books
WHERE pages IS NOT NULL
""")

pages = [row[0] for row in cursor.fetchall()]



fig, axs = plt.subplots(1, 3, figsize=(18, 5))


# Chart 1: Top Books

axs[0].bar(titles, ratings)
axs[0].set_title("Top Rated Books")
axs[0].tick_params(axis='x', rotation=45)


# Chart 2: Top Genres

axs[1].bar(genre_labels, genre_values)
axs[1].set_title("Top Genres")
axs[1].tick_params(axis='x', rotation=45)


# Chart 3: Page Distribution

axs[2].hist(pages, bins=10)
axs[2].set_title("Page Count Distribution")

plt.tight_layout()
plt.show()

conn.close()
