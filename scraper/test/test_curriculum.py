import pytest
from bs4 import BeautifulSoup

from scraper.curriculum import parse_program, parse_courselist


def conc_laes_cgraph():
    with open('resources/conc-laes-cgraph.html') as file:
        text = file.read()
    soup = BeautifulSoup(text, features='html.parser')
    return soup.find('table', attrs={'class': 'sc_courselist'})


def qs_minor():
    with open('resources/queer-studies-minor.html') as file:
        text = file.read()
    soup = BeautifulSoup(text, features='html.parser')
    return soup.find('table', attrs={'class': 'sc_courselist'})


conc_laes_cgraph = conc_laes_cgraph()
qs_minor = qs_minor()


@pytest.mark.parametrize('tag,count', [
    (conc_laes_cgraph, 9),
    (qs_minor, 9),
])
def test_parse_courselist(tag, count):
    gen = parse_courselist(tag)
    assert len(gen) == count

