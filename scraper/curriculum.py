import asyncio
import logging
import re
from collections import namedtuple
from typing import List, Union

import aiohttp
from bs4 import Tag, NavigableString, BeautifulSoup

from scraper.data import Subject

logger = logging.getLogger(__name__)


RawCourse = namedtuple('RawCourse', 'course')
OrCourse = namedtuple('OrCourse', 'course')
SelectFromTheFollowing = namedtuple('SelectFromTheFollowing', 'units courses')
AreaHeader = namedtuple('AreaHeader', 'text')
Comment = namedtuple('Comment', 'comment')
TotalUnits = namedtuple('TotalUnits', 'units')
Token = Union[RawCourse, OrCourse, SelectFromTheFollowing, AreaHeader, Comment, TotalUnits]


class InvalidCourseException(Exception):
    pass


def read_course(row: Tag):
    try:
        a = row.findChild('a')
        js = a.attrs.get('onclick')
        match = re.match(r'return showCourse\(this, \'(.*)\'\);', js)
        return match.group(1)
    except:
        raise InvalidCourseException()


def lex_courselist(tag: Tag):
    rch = list(tag.find('tbody').children)
    rows = iter(rch)
    try:
        while True:
            row = next(rows)
            if isinstance(row, NavigableString):
                continue
            row: Tag
            css_classes = row.attrs.get('class')

            if 'listsum' in css_classes:
                hourscol = row.findChild('td', {'class': 'hourscol'})
                yield TotalUnits(int(hourscol.contents[0]))
            elif 'areaheader' in css_classes:
                span = row.findChild('span')
                yield AreaHeader(span.contents[0])
            elif 'orclass' in css_classes:
                yield OrCourse(read_course(row))
            else:
                courselistcomment = row.findChild('span', {'class': 'courselistcomment'})
                if courselistcomment:
                    yield SelectFromTheFollowing(3, [])
                else:
                    yield RawCourse(read_course(row))
    except StopIteration:
        return


def parse_program(html_text):
    soup = BeautifulSoup(html_text, features='html.parser')

    subjects_list = soup.find('ul', attrs={'class': 'sc_courselist'})
    pass