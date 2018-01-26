from sample import jasssScrap
from bs4 import BeautifulSoup

soup = BeautifulSoup(jasssScrap.visit_article(1, 1, 1), 'html5lib')

# print(soup.prettify())

title_tag = soup.find(jasssScrap.meta_tag, {jasssScrap.meta_name: jasssScrap.meta["title"]})
tags_tag = soup.find(jasssScrap.meta_tag, {jasssScrap.meta_name: jasssScrap.meta["tags"]})

print("The article title is: " + title_tag[jasssScrap.meta_content] + "\n" + "With given key words: " + str(
    jasssScrap.get_tags(tags_tag[jasssScrap.meta_content])))