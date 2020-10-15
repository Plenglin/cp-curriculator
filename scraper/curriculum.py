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
IndentCourse = namedtuple('IndentCourse', 'course')
SelectFromTheFollowing = namedtuple('SelectFromTheFollowing', 'units')
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
    for row in rch:
        if isinstance(row, NavigableString):
            continue
        row: Tag
        css_classes = row.attrs.get('class')

        if 'listsum' in css_classes:
            hourscol = row.findChild('td', {'class': 'hourscol'})
            yield TotalUnits([int(x) for x in hourscol.contents[0].split('-')])
        elif 'areaheader' in css_classes:
            span = row.findChild('span')
            yield AreaHeader(span.contents[0])
        elif 'orclass' in css_classes:
            yield OrCourse(read_course(row))
        else:
            courselistcomment = row.findChild('span', {'class': 'courselistcomment'})
            if courselistcomment:
                if 'select from the following:' in courselistcomment.contents[0].lower():
                    units = row.findChild('td', {'class': 'hourscol'}).contents[0]
                    yield SelectFromTheFollowing(int(units))
                else:
                    yield Comment(courselistcomment.contents[0])
            else:
                if row.findChild('div', {'style': 'margin-left: 20px;'}):
                    yield IndentCourse(read_course(row))
                else:
                    yield RawCourse(read_course(row))


OrRequirement = namedtuple('Requirement', 'units courses')


class CourseListParser:
    def __init__(self, tokens: List[Token]):
        self.i = 0
        self.tokens = tokens

    def read(self):
        out = self.tokens[self.i]
        self.i += 1
        return out

    def peek(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return None

    def read_raw_course(self, head: RawCourse):
        group = [head.course]
        while isinstance(self.peek(), OrCourse):
            group.append(self.read().course)
        return OrRequirement(4 * len(group), group)

    def read_courses_run(self):
        out = []
        while self.peek():
            token = self.read()
            if isinstance(token, RawCourse):
                out.append(self.read_raw_course(token))
            elif isinstance(token, SelectFromTheFollowing):
                pass


    def read_select_from_the_following(self, sftf: SelectFromTheFollowing):
        group = [head.course]
        while isinstance(self.peek(), OrCourse):
            group.append(self.read().course)
        return OrRequirement(4 * len(group), group)


    def read_courselist(self):
        out = []
        while self.peek():
            token = self.read()
            if isinstance(token, RawCourse):
                out.append(self.read_raw_course(token))
            elif isinstance(token, SelectFromTheFollowing):
                token.units


def parse_program(html_text):
    soup = BeautifulSoup(html_text, features='html.parser')

    subjects_list = soup.find('ul', attrs={'class': 'sc_courselist'})
    pass