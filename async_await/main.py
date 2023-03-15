import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()

async def scrape(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(fetch(url, session)))
        pages = await asyncio.gather(*tasks)

        for page in pages:
            soup = BeautifulSoup(page, 'html.parser')
            title = soup.title.string
            print(title)

if __name__ == '__main__':
    urls = ['https://www.google.com', 'https://www.yahoo.com', 'https://www.bing.com', 'https://www.python.org', 'https://www.github.com']
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape(urls))