# wikipedia_scraper
A scraper for wikipedia that downloads webpages and the links to other pages and stores them in a sqlite database.
This scraper starts on the wikipedia page on the usa. It then scrapes all links on that page and adds to a sqlite database. On every additional time it is run, it scrapes 100 pages at a time, adding the links to the database.
To run, enter at the terminal python3 async_scraper.py with an optional command line argument of an integer representing how many cycles to run (The default is one). 
See requirements.txt for the necessary packages.
