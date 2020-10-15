from unittest import TestCase

import pytest

from .courses import parse_coursesaz, parse_single_subject
from .data import Course, Subject
from .test_resources import resolve_test_resource


def test_parse_coursesaz():
    with open(resolve_test_resource('coursesaz.html')) as file:
        text = file.read()

    subjects = parse_coursesaz(text)

    for subj in subjects:
        assert isinstance(subj, Subject)
        assert subj.href
        assert subj.name
        assert subj.code


@pytest.mark.parametrize("pathname", [
    'wgs-catalog.html',
    'math-catalog.html',
])
def test_parse_single_subject(pathname):
    with open(resolve_test_resource(pathname)) as file:
        text = file.read()

    courses = parse_single_subject(text)

    for course in courses:
        assert isinstance(course, Course)
        assert course.name
        assert course.number
        assert course.subject
