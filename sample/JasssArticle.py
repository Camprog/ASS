import jasssScrap
import requests
from bs4 import BeautifulSoup


class JasssArticle:

    def __init__(self, volume=1, issue=1, article=1):
        """init article from JASSS based on the value of volume, number and article

        :param int volume:
        :param int number:
        :param int article:
        """
        basic_url = jasssScrap.base_url + str(volume) + jasssScrap.separator + str(issue) + jasssScrap.separator
        req = requests.get(basic_url + str(article) + jasssScrap.html)
        self.url = req.url
        if req.status_code == requests.codes.ok:
            self.bs_article = BeautifulSoup(req.content, 'html5lib')
        else:
            self.bs_article = BeautifulSoup(requests.get(basic_url + str("review" + article) + jasssScrap.html), 'html5lib')

    def __repr__(self):
        return self.url

    def is_review(self):
        """ Tells if this article is a review or not """
        return True if self.__repr__().contains("review") else False

    def get_key_worlds(self):
        """
        Get the key worlds from an article

        :param html bs_article:
        :return: a tuple made of key worlds
        """
        return [x.strip() for x in self.get_content_with_tag("tags").split(',')]

    def get_title(self):
        """ Retrieve the title of the article """
        return self.get_content_with_tag()

    def get_authors(self):
        """
        Retrieve the authors of the article

        :param html bs_article:
        :return: a tuple of authors
        """
        return [x.strip() for x in self.get_content_with_tag("authors").split(';')]

    def get_abstract(self):
        """ Retrieve the abstract of the article"""
        the_abstract = self.get_content_with_tag("abstract")

        if len(the_abstract.split()) < 5:
            return str(self.bs_article.find(string="Abstract").findNext("dl").next.contents[0]).strip()
        return the_abstract

    def get_content_with_tag(self, tag="title"):
        """
        Retrieve the content of a tag as define by *beautifulsoup*

        :param html bs_article: the soup
        :param string tag: the tag to find in the soup
        :return: a string representation of the content of the tag
        """
        return self.bs_article.find(jasssScrap.jasss_meta_tag, {jasssScrap.jasss_meta_name:
                                                              jasssScrap.meta[tag]})[jasssScrap.jasss_meta_content]