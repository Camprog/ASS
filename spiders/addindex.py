from scraping import WebScraping
"""Article Search and Scraping (ASS)"""
class Addindex():

    def __init__(self, url):
        self.url = url

    def Add(self):
        WebScraping.start_urls.append(self.url)
        print(WebScraping.start_urls)
        return WebScraping.start_urls

Newurl = Addindex('http://www.jeuxvideo.com/sorties/dates-de-sortie.htm')
Newurl.Add()