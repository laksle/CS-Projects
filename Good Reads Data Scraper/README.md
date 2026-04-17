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

