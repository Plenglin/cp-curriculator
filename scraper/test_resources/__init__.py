import os
from typing import List

from bs4 import BeautifulSoup, Tag

from scraper.curriculum import RawCourse, TotalUnits, AreaHeader, OrCourse, SelectFromTheFollowing, \
    Comment


def get_courselist(path) -> List[Tag]:
    path = os.path.realpath(__file__ + '/../' + path)
    with open(path) as file:
        text = file.read()
    soup = BeautifulSoup(text, features='html.parser')
    return soup.findAll('table', attrs={'class': 'sc_courselist'})


conc_laes_cgraph, = get_courselist('conc-laes-cgraph.html')
qs_minor, = get_courselist('queer-studies-minor.html')
math_major, math_ge = get_courselist('bs-math.html')

conc_laes_cgraph_lexed = [
    RawCourse('CSC 101'),
    RawCourse('CSC 202'),
    RawCourse('CSC 203'),
    RawCourse('CSC 123'),
    RawCourse('CSC 225'),
    RawCourse('CSC 303'),
    RawCourse('CSC 348'),
    RawCourse('CSC 357'),
    RawCourse('CSC 471'),
    TotalUnits(34)
]
qs_minor_lexed = [
    AreaHeader(text='Required Courses'),
    RawCourse(course='WGS 302'),
    OrCourse(course='ES 345'),
    RawCourse(course='WGS 455'),
    AreaHeader(text='Core Courses'),
    SelectFromTheFollowing(units=8),
    RawCourse(course='ANT 460'),
    RawCourse(course='ENGL 382'),
    RawCourse(course='ES 325'),
    RawCourse(course='HIST 458'),
    RawCourse(course='WGS 340'),
    AreaHeader(text='Approved Electives'),
    SelectFromTheFollowing(units=8),
    RawCourse(course='ANT 344'),
    RawCourse(course='ANT 393'),
    RawCourse(course='ANT 425'),
    RawCourse(course='BIO 123'),
    Comment(comment='300 and 400-level English Topics/Subtitle courses as approved'),
    RawCourse(course='ES 112'),
    OrCourse(course='ES 241'),
    OrCourse(course='ES 242'),
    OrCourse(course='ES 243'),
    OrCourse(course='ES 244'),
    RawCourse(course='ES 311'),
    RawCourse(course='ES 340'),
    OrCourse(course='ES 380'),
    OrCourse(course='ES 381'),
    RawCourse(course='HIST 216'),
    RawCourse(course='HIST 433'),
    OrCourse(course='HIST 459'),
    RawCourse(course='ISLA 320'),
    RawCourse(course='KINE 323'),
    RawCourse(course='PHIL 336'),
    RawCourse(course='POLS 310'),
    RawCourse(course='PSY 304'),
    RawCourse(course='PSY 324'),
    RawCourse(course='PSY 475'),
    RawCourse(course='RELS 370'),
    RawCourse(course='SOC 306'),
    OrCourse(course='SOC 327'),
    RawCourse(course='SOC 311'),
    RawCourse(course='TH 305'),
    RawCourse(course='WGS 270'),
    RawCourse(course='WGS 320'),
    RawCourse(course='WGS 375'),
    RawCourse(course='WGS 400'),
    RawCourse(course='WGS 401'),
    RawCourse(course='WGS 467'),
    RawCourse(course='WGS 470'),
    TotalUnits(units=24)
]
math_major_lexed = [
    AreaHeader(text='MAJOR COURSES'),
    RawCourse(course='MATH 141'),
    RawCourse(course='MATH 142'),
    RawCourse(course='MATH 143'),
    RawCourse(course='MATH 202'),
    RawCourse(course='MATH 206'),
    RawCourse(course='MATH 241'),
    RawCourse(course='MATH 242'),
    RawCourse(course='MATH 248'),
    RawCourse(course='MATH 306'),
    RawCourse(course='MATH 336'),
    RawCourse(course='MATH 412'),
    SelectFromTheFollowing(units=4),
    RawCourse(course='MATH 459'),
    RawCourse(course='MATH 460'),
    RawCourse(course='MATH 461'),
    RawCourse(course='MATH 481'),
    RawCourse(course='CSC 101'),
    RawCourse(course='PHYS 141'),
    SelectFromTheFollowing(units=4),
    RawCourse(course='PHYS 132'),
    RawCourse(course='PHYS 133'),
    Comment(comment='General Curriculum in BS Mathematics or Concentration'),
    AreaHeader(text='GENERAL EDUCATION (GE)'),
    Comment(comment='(See GE program requirements below.)'),
    AreaHeader(text='FREE ELECTIVES'),
    Comment(comment='Free Electives'),
    TotalUnits(units=180)
]
math_ge_lexed = [
    AreaHeader(text='Area A'),
    Comment(comment='A1'),
    Comment(comment='A2'),
    Comment(comment='A3'),
    AreaHeader(text='Area B'),
    Comment(comment='B1'),
    Comment(comment='B2'),
    Comment(comment='B3'),
    Comment(comment='B4'),
    Comment(comment='Upper-Division B'),
    AreaHeader(text='Area C'),
    Comment(comment='Lower-division courses in Area C must come from three different subject prefixes.'),
    Comment(comment='C1'),
    Comment(comment='C2'),
    Comment(comment='Lower-Division C Elective - Select a course from either C1 or C2'),
    Comment(comment='Upper-Division C'),
    AreaHeader(text='Area D'),
    Comment(comment='D1'),
    Comment(comment='D2'),
    Comment(comment='Upper-Division D'),
    AreaHeader(text='Area E'),
    Comment(comment='Lower-Division E'),
    AreaHeader(text='GE Electives in Areas B, C, and D'),
    Comment(comment='Select courses from two different areas; may be lower-division or upper-division courses.'),
    Comment(comment='GE Electives (4 units in Major plus 4 units in GE)'),
    TotalUnits(units=60)
]
