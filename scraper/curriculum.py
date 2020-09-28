import asyncio
import logging
import re
from collections import namedtuple
from typing import List

import aiohttp
from bs4 import Tag, NavigableString, BeautifulSoup

from scraper.data import Subject

logger = logging.getLogger(__name__)


class WebpageChangedException(Exception):
    pass


def read_course(row: Tag):
    codecol = row.find('td')
    js = codecol.find('a').attrs.get('onclick')
    match = re.match(r'return showCourse\(this, \'(.*)\'\);', js)
    return match.group(1)

def parse_courselist(tag: Tag):
    rch = list(tag.find('tbody').children)
    rows = iter(rch)
    reqs = []
    try:
        while True:
            row = next(rows)
            if isinstance(row, NavigableString):
                continue
            row: Tag
            reqs.append(read_course(row))
    except StopIteration:
        return


def parse_program(html_text):
    soup = BeautifulSoup(html_text, features='html.parser')

    subjects_list = soup.find('ul', attrs={'class': 'sc_courselist'})
    pass