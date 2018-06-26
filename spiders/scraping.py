import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from urllib.parse import urlparse
from scrapy.utils.project import get_project_settings
from scrapy.selector import HtmlXPathSelector

# install pywin32
# CD .\spiders
# scrapy runspider scraping.py

class WebScraping(scrapy.Spider):
    name = "scraping"
    start_urls = ['http://jasss.soc.surrey.ac.uk/index_by_issue.html','https://www.comses.net/codebases/', 'http://www.jeuxvideo.com/sorties/dates-de-sortie.htm', 'https://myanimelist.net/topmanga.php']

    le1 = LinkExtractor(canonicalize=True, unique=False)
    rules = [
        Rule(
            le1,
            follow=True,
            callback="parse_items"
        )
    ]

    def __init__(self, keyword, search):
        self.keyword = keyword
        self.search=search


    def start_requests(self):
        print(self.start_urls)
        self.items = dict()
        url = input ("Index, enter n° : ")
        self.start_urls = self.start_urls[int(url)]

        """Give Domain with URL"""
        parsed_uri = urlparse(self.start_urls)
        self.domain = parsed_uri.netloc

        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    # the response containing a HTML form
    def parse(self, response):
        # extract data from every links
        links = self.le1.extract_links(response)

        if self.search == "deep":
            """Body of article content"""
            for link in links:
                self.items['content'] = response.xpath('//body//p//text()').extract()
                print(self.items['content'])



        else:
            for link in links:
                # print(link.url, link.text)
                """ match URL with title and put them in a dict"""
                if self.keyword in link.text.lower():
                    self.items[link.url] = link.title
                    print(link.title, link.url)

        # follow next page
        try:
            #this response use css, only for comses.net /// Change page-item to adapt
            next_page = response.css('li.page-item a::attr("href")').extract()[-1]
            #next_page = response.xpath('').extract()
            #next_page = response.css('div.pagi-suivant-actif a::attr("href")').extract()[-1]
            print(next_page)
            if next_page:
                next_page = "https://" + self.domain + next_page
                print(next_page)
                yield response.follow(next_page, self.parse)
        except:
            print("there isn't other page")


    def AddIndex(self, Newindex):
        self.start_urls.append(Newindex)
        return self.start_urls


#Launch spider
if __name__ == "__main__":

    process = CrawlerProcess()
    """keyword to do a keyword search,search=deep to a deep search"""
    process.crawl(WebScraping,keyword="", search="deep")
    process.start()



    """Add an index in list"""
"""
    A = WebScraping()
    A.AddIndex('http://www.jeuxvideo.com/sorties/dates-de-sortie.htm')
"""





