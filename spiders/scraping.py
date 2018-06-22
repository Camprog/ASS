import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from urllib.parse import urlparse
from scrapy.utils.project import get_project_settings

# install pywin32
# CD .\spiders
# scrapy runspider scraping.py

class WebScraping(scrapy.Spider):
    name = "scraping"
    start_urls = ['http://jasss.soc.surrey.ac.uk/index_by_issue.html','https://www.comses.net/codebases/']

    le1 = LinkExtractor(canonicalize=True, unique=False)
    rules = [
        Rule(
            le1,
            follow=True,
            callback="parse_items"
        )
    ]

    def start_requests(self):
        self.a=""
        self.items = dict()
        print (self.start_urls)

        url = input ("Index, enter n° : ")
        self.start_urls = self.start_urls[int(url)-1]


        """Give Domain with URL"""
        parsed_uri = urlparse(self.start_urls)
        self.domain=parsed_uri.netloc


        for url in WebScraping.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # the response containing a HTML form
    def parse(self, response):
        #extract data from every links
        links = self.le1.extract_links(response)

        body = input("d to do a deeper search, enter to a normal scan :")

        if body == "d":
            """Body of article content"""
            for link in links:
                print(response.xpath('//body//div//text()').extract())
        else:
            for link in links:
                # print(link.url, link.text)
                """ match URL with title and put them in a dict"""
                if self.a in link.text.lower():
                    self.items[link.url] = link.text
                    print(link.text, link.url)

        # follow next page
        try:
            #this response use css, only for comses.net
            next_page = response.css('li.page-item a::attr("href")').extract()[-1]
            #next_page = response.css('a.pagi-suivant-actif a::attr("href")').extract()[-1]

            if next_page:
                # print(next_page)
                next_page = self.domain + next_page
                yield response.follow(next_page, self.parse)
        except:
            print("there isn't other page")


    def AddIndex(self, Newindex):
        print (self.start_urls)
        self.start_urls.append(Newindex)
        return self.start_urls


#Launch spider
if __name__ == "__main__":
    """Add an index in list"""


    A = WebScraping()
    A.AddIndex('http://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm')


    process = CrawlerProcess()
    process.crawl(WebScraping)
    process.start()

    """
    liste des index
    'http://jasss.soc.surrey.ac.uk/index_by_issue.html'
    'https://www.comses.net/codebases/'
    """



