import asyncio
import logging

from scraper.scrape import fetch_all_courses

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    out = asyncio.run(fetch_all_courses())
    print(out)
