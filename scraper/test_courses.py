from unittest import TestCase

import pytest

from scraper.courses import parse_coursesaz, parse_single_subject
from scraper.data import Course, Subject


def test_parse_coursesaz():
    with open('test_resources/coursesaz.html') as file:
        text = file.read()

    subjects = parse_coursesaz(text)

    for subj in subjects:
        assert isinstance(subj, Subject)
        assert subj.href
        assert subj.name
        assert subj.code


@pytest.mark.parametrize("pathname", [
    'test_resources/wgs-catalog.html',
    'test_resources/math-catalog.html',
])
def test_parse_single_subject(pathname):
    with open(pathname) as file:
        text = file.read()

    courses = parse_single_subject(text)

    for course in courses:
        assert isinstance(course, Course)
        assert course.name
        assert course.number
        assert course.subject
