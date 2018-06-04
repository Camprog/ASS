from sample import JasssArticle
from itertools import product

base_url = "http://jasss.soc.surrey.ac.uk/"
separator = '/'
html = ".html"

jasss_meta_tag = "meta"
jasss_meta_name = "name"
jasss_meta_content = "content"

meta = {"title": "DC.Title",
        "authors": "DC.Creator",
        "abstract": "DC.Description",
        "date": "DC.Date",
        "tags": "DC.Subject"}


def visit_article(volume=1, number=1, article=1):
    """Retrieve article from JASSS based on the value of volume, number and article

    :param int volume:
    :param int number:
    :param int article:
    :return: an html page that represents requested article
    """
    return JasssArticle(volume, number, article)


def visit_articles(to_volume=1, to_number=4, to_article=1):
    """Retrieve a collection of articles from 1 to args volume, issue and article found in JASSS

    :param int to_volume: the max number of volume; between 1 and ongoing number of volume
    :param int to_number: the max number of issue; between 1 and 4
    :param int to_article: the max number of article; between 1 and the number of article for current volume and issue
    :return: a tuple made of html pages
    """
    return [visit_article(x, y, z) for x, y, z in
            product(range(to_volume), range(to_number), range(to_article))]

