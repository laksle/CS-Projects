import sqlite3

conn = sqlite3.connect("goodreads.db")
cursor = conn.cursor()
print("\nOverall Table Data:\n")
cursor.execute("""
SELECT * FROM books
""")
for row in cursor.fetchall():
    print(row)
print("\nOverall Genre Data:\n")
cursor.execute("""SELECT * FROM genres""")
for row in cursor.fetchall():
    print(row)


print("\nTop Rated Books by Genre:\n")
cursor.execute("""
SELECT 
    g.name AS genre,
    AVG(b.rating) AS avg_rating
FROM books b
JOIN book_genres bg ON b.id = bg.book_id
JOIN genres g ON g.id = bg.genre_id
WHERE b.rating IS NOT NULL
GROUP BY g.name
ORDER BY avg_rating DESC
LIMIT 10;
""")

for row in cursor.fetchall():
    print(row)

conn.close()
