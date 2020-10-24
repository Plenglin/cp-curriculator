import asyncio
import logging
import re
from collections import namedtuple
from typing import List, Union, Generator, Iterable

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


def lex_courselist(tag: Tag) -> Generator[Token]:
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


Mono = namedtuple('Mono', 'course')
Or = namedtuple('Or', 'requirements')
And = namedtuple('And', 'requirements')
SFTF = namedtuple('SFTF', 'units requirements')
Requirement = Union[Mono, Or, And, SFTF]

# Pseudotoken
IndentedSFTFToken = namedtuple('IndentedSFTFToken', 'sftf')


def parse_courselist(tokens: Iterable[Token]) -> Requirement:
    stack = []
    root = []
    for token in tokens:
        if isinstance(token, Comment):
            continue

        # End of IndentCourse chain
        if isinstance(stack[-1], OrCourse) and not isinstance(token, OrCourse):
            group = []
            while isinstance(stack[-1], IndentCourse):
                pass

        # End of OrCourse chain
        if isinstance(stack[-1], OrCourse) and not isinstance(token, OrCourse):
            group = []
            while isinstance(stack[-1], OrCourse):
                group.append(stack.pop())
            group.append(stack.pop())  # Pop the heading RawCourse
            group.reverse()
            root.append(OrCourse(group))

        if isinstance(token, IndentCourse):
            stack.append(token)
        elif isinstance(token, RawCourse):
            if isinstance(stack[-1], RawCourse):
                yield stack.pop()
                stack.append(token)
        elif isinstance(token, OrCourse):
            stack.append(token)
        elif isinstance(token, SelectFromTheFollowing):
            stack.append(token)


def parse_program(html_text):
    soup = BeautifulSoup(html_text, features='html.parser')

    subjects_list = soup.find('ul', attrs={'class': 'sc_courselist'})
    pass
