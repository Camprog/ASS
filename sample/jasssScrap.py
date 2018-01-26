import requests
import itertools

base_url = "http://jasss.soc.surrey.ac.uk/"
separator = '/'
html = ".html"

meta_tag = "meta"
meta_name = "name"
meta_content = "content"

meta = {"title": "DC.Title",
        "authors": "DC.Creator",
        "abstract": "DC.description",
        "data": "DC.Date",
        "tags": "DC.Subject"}



def visit_article(volume=1, number=1, article=1):
    """visit url page for an article of JASSS"""
    return requests.get(base_url + str(volume)
                        + separator + str(number)
                        + separator + str(article)
                        + html).content

def visit_articles(to_volume=1, to_number=4, to_article=1):
    return [visit_article(x,y,z) for x,y,z in itertools.product(range(to_volume), range(to_number), range(to_article))]


def get_tags(tags):
    return [x.strip() for x in tags.split(',')]
