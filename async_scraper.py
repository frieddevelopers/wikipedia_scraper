import asyncio 
import aiohttp 
import sys
from sqlite3 import OperationalError
from scraper import get_random_urls, get_links, start_database, insert_into_db, insert_pages



async def main():
    try:
        urls = get_random_urls(100)
        if len(urls) < 1:
            urls = ["https://en.wikipedia.org/wiki/United_States",]
    except OperationalError:
        urls = ["https://en.wikipedia.org/wiki/United_States",]
    async with aiohttp.ClientSession() as session:
        tasks = [download_pages(url, session) for url in urls]
        pages = await asyncio.gather(*tasks)

    links = []
    conn, cur = start_database()
    print("Parsing pages....")
    for page in pages:
        links += get_links(page[0], page[1])
    insert_pages(pages, conn, cur)

    
    links = set(links) 
    insert_into_db(links, cur, conn)



async def download_pages(link, session):
    print(f"Requesting {link}")
    async with session.get(link) as response:
        text = await response.text()
        return text, link


if len(sys.argv) == 2:
    try:
        count = int(sys.argv[1])
    except ValueError:
        sys.exit("Invalid command line argument")
else:
    count = 1
for i in range(count):
    asyncio.run(main())