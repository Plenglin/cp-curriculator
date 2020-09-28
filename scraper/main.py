import asyncio
import logging

from scraper.courses import fetch_all_courses
from scraper.curriculum import parse_programsaz

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    out = asyncio.run(parse_programsaz())
    print(out)
