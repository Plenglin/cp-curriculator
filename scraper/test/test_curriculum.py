from bs4 import BeautifulSoup

from scraper.curriculum import parse_program, parse_courselist


def test_parse_courselist():
    with open('resources/conc-laes-cgraph.html') as file:
        text = file.read()
    soup = BeautifulSoup(text, features='html.parser')
    courselist = soup.find('table', attrs={'class': 'sc_courselist'})

    gen = parse_courselist(courselist)
    print(gen)

