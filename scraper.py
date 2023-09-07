import sqlite3
from bs4 import BeautifulSoup 
from urllib.parse import urljoin
import re

def scrape_page(url):
    """
    This function takes in a url and returns the url's html content and the url (in a tuple).
    """
    print(f"Downloading {url}")
    data = requests.get(url, timeout=10)
    return data.content, url

def get_links(page, url):
    """
    This function takes in an html page and the link of the page and returns all wikipedia links in the page (in a list).
    """
    li_links = []
    soup = BeautifulSoup(page, "html.parser")
    links = soup.find_all("a")
    for link in links:
        i = link.get("href")
        if validate_link(i):
            li_links.append(urljoin(url, i))

    return li_links



def validate_link(link):
    """
    This is a helper function for the get_links to help scrape all the links that link to other wikipedia pages. It returns True if it is a wikipedia link and False if not.
    """
    try:
        pattern = r"^/wiki[^:\(]+$"
        return bool(re.search(pattern, link))
    except TypeError:
        return None


def insert_into_db(links, cur="", conn=""):
    """
    This function takes in a url, webpage, list of links, a sqlite cursor object (optional), and a sqlite connection object (optional).
    It then inserts all the unique links into the the data.db database.
    """
    print("Adding links to the database")
    links = set(links)
    if not cur or not conn:
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
    

    # Loop through links, inserting into database 
    count = 0 
    for link in links:
        cur.execute("INSERT OR IGNORE INTO links (link) VALUES (?);", (link,))

        count += 1 
        if count == 100:
            conn.commit()
            count = 0

    conn.commit()


def insert_pages(links, conn, cur):
    """
    This function adds the html of the downloaded pages to the database.
    """
    for page in links:
        cur.execute("UPDATE links SET page = ? WHERE link = ?;", (page[0], page[1]))
    conn.commit()

def start_database():
    """
    This function starts a database if it doesn't exist. It returns a cursor and connection object.
    """
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY AUTOINCREMENT, link VARCHAR(250) UNIQUE NOT NULL, page TEXT DEFAULT(NULL));")
    conn.commit()
    return (conn, cur)


def get_random_urls(amount=200):
    """
    This function fetches a list of links from the database that weren't yet downloaded. It takes an optional parameter amount for how many links to fetch. It returns a list of links.
    """
    print("Fetching links from database.")
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT link FROM links WHERE page IS NULL LIMIT ?", (amount,))
    links = cur.fetchall()
    links = [i[0] for i in links]
    return links

