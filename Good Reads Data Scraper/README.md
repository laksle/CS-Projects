This project scrapes individual book information from a Goodreads list, stores it in a SQLite database, and generates analytical visualizations.

Technology Used:
- Python  
- Selenium (web scraping automation)  
- BeautifulSoup (HTML parsing)  
- SQLite (database)  
- SQL (data querying & aggregation)  
- Matplotlib (data visualization)  

Project Structure:
- database.py → Creates and initializes the SQLite database  
- scraper.py → Scrapes Goodreads book data and inserts it into the database  
- chart.py → Produces visual analytics for: Top rated books, Most frequent genres, and Page count distribution  

Testing Instructions:

First, install the dependencies by running:
**pip install selenium beautifulsoup4 matplotlib**

Then run:
**python scraper.py**

To generate an optional chart, run:
**python chart.py**

These are the sample results for the [Best Sci-Fi/Fantasy Short Stories](https://www.goodreads.com/list/show/161527.Best_Sci_fi_Fantasy_Short_Story_Collections) List in Goodreads:
These 2 images are the books and genres tables for the list 
<img width="1744" height="466" alt="Screenshot 2026-04-17 200522" src="https://github.com/user-attachments/assets/64134209-9a67-4cde-937b-263195f4bfdf" />
<img width="352" height="550" alt="Screenshot 2026-04-17 200648" src="https://github.com/user-attachments/assets/6d7fd142-17d8-4ce8-8498-349c42184e47" />

The generated charts for this data is listed in the image below
<img width="1800" height="500" alt="mycharts" src="https://github.com/user-attachments/assets/4b3fc5a1-322e-4863-95c0-0fe4eb9c3433" />


