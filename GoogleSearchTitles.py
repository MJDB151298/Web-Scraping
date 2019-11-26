from bs4 import BeautifulSoup as soup
import requests
"""
    Insert link from a google search, return the titles of the first page.
"""


def getTitles():
    link_input = input()
    google_search = ''
    titles = []
    for x in link_input:
        if '"' not in x:
            google_search += x

    r = requests.get(google_search)
    page_soup = soup(r.text, features="lxml")

    data = page_soup.findAll('h3', {'class': 'r'})
    for x in data:
        titles.append(x.text)
    return titles
