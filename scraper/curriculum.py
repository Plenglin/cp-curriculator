import asyncio
import logging
import re
from collections import namedtuple
from typing import List, Union

import aiohttp
from bs4 import Tag, NavigableString, BeautifulSoup

from scraper.data import Subject

logger = logging.getLogger(__name__)


class InvalidCourseException(Exception):
    pass


def read_course(row: Tag):
    try:
        codecol = row.find('td')
        a = codecol.find('a')
        js = a.attrs.get('onclick')
        match = re.match(r'return showCourse\(this, \'(.*)\'\);', js)
        return match.group(1)
    except:
        raise InvalidCourseException()


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
            classes = row.attrs.get('class')

            if 'listsum' in classes or 'areaheader' in classes:
                continue

            reqs.append(read_course(row))
    except StopIteration:
        return reqs


def parse_program(html_text):
    soup = BeautifulSoup(html_text, features='html.parser')

    subjects_list = soup.find('ul', attrs={'class': 'sc_courselist'})
    pass