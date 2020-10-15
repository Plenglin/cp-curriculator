import asyncio
import logging
import re
from typing import List

import aiohttp
import bs4
from bs4 import Tag, NavigableString

from scraper.data import Course, Subject

logger = logging.getLogger(__name__)


class WebpageChangedException(Exception):
    pass


def parse_coursesaz(html_text):
    soup = bs4.BeautifulSoup(html_text, features='html.parser')

    subjects_list = soup.find('ul', attrs={'id': '/coursesaz/'})
    for child in subjects_list.children:
        if isinstance(child, NavigableString):
            continue
        child: Tag

        href = next(child.children).attrs['href']
        match = re.match(r'(.+) \(([A-Z]+)\)', child.text)
        if match is None:
            raise WebpageChangedException

        name, code = match.groups()

        yield Subject(name, code, href)


def parse_single_subject(html_text):
    soup = bs4.BeautifulSoup(html_text, features='html.parser')
    courseblocks = soup.findAll(attrs={'class': 'courseblock'})

    for block in courseblocks:
        block: Tag
        title_line = block.find(attrs={'class': 'courseblocktitle'}).text.replace(u'\xa0', ' ')

        match = re.search(r'(\w+) (\d+)\. (.+)\.', title_line)
        if match is None:
            raise WebpageChangedException

        subject, number, title = match.groups()
        yield Course(subject, int(number), title)


async def parse_and_scrape_coursesaz(session):
    async with session.get('http://catalog.calpoly.edu/coursesaz/') as resp:
        text = await resp.text()
    return parse_coursesaz(text)


async def parse_and_scrape_course(session, pathname):
    async with session.get('http://catalog.calpoly.edu' + pathname) as resp:
        text = await resp.text()
        logger.debug('Fetched %s', pathname)
    return parse_single_subject(text)


async def fetch_all_courses():
    async with aiohttp.ClientSession() as session:
        subjects: List[Subject] = list(await parse_and_scrape_coursesaz(session))
        fetchers = [parse_and_scrape_course(session, subject.href) for subject in subjects]
        course_groups: List[List[Course]] = [list(courses) for courses in await asyncio.ensure_future(asyncio.gather(*fetchers))]

        logger.info('Downloaded %s courses across %s subjects', sum(len(group) for group in course_groups), len(subjects))

        return {
            subject.code: {
                'code': subject.code,
                'name': subject.name,
                'courses': {
                    course.number: {
                        'subject': course.subject,
                        'number': course.number,
                        'name': course.name
                    } for course in courses
                }
            }
            for subject, courses in zip(subjects, course_groups)
        }
