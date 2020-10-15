import pytest
from bs4 import BeautifulSoup

from scraper.curriculum import lex_courselist, RawCourse, TotalUnits


def conc_laes_cgraph():
    with open('test_resources/conc-laes-cgraph.html') as file:
        text = file.read()
    soup = BeautifulSoup(text, features='html.parser')
    return soup.find('table', attrs={'class': 'sc_courselist'})


def qs_minor():
    with open('test_resources/queer-studies-minor.html') as file:
        text = file.read()
    soup = BeautifulSoup(text, features='html.parser')
    return soup.find('table', attrs={'class': 'sc_courselist'})


conc_laes_cgraph = conc_laes_cgraph()
qs_minor = qs_minor()


@pytest.mark.parametrize('tag,tokens', [
    (conc_laes_cgraph, [
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
    ]),
    (qs_minor, 9),
])
def test_lex_courselist(tag, tokens):
    gen = lex_courselist(tag)
    actual = list(gen)
    assert actual == tokens

