from sample import jasssScrap
from bs4 import BeautifulSoup

soup = BeautifulSoup(jasssScrap.visit_article(1, 1, 1), 'html5lib')

# print(soup.prettify())

title = jasssScrap.get_title(soup)
key_worlds = jasssScrap.get_key_worlds(soup)
authors = jasssScrap.get_authors(soup)

print("The first article published article in JASSS was: " + title + "\n" + "The key words was: " + str(
    key_worlds) + "\n" + "And authors was: " + str(authors))
