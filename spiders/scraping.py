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
    le1 = LinkExtractor(canonicalize=True, unique=False, allow=('https://www.comses.net/codebases/', 'http://jasss.soc'
                                                                                                     '.surrey.ac.uk/'),
                        deny=('/?tags'))
    rules = [
        Rule(
            le1,
            follow=True,
            callback="parse_items"
        )
    ]

    def start_requests(self):
        #dict to storage url + title
        self.a = "agent-based"
        self.items = dict()
        self.start_urls = ['http://jasss.soc.surrey.ac.uk/index_by_issue.html', 'https://www.comses.net/codebases/']
        return self.start_urls
        print(self.start_urls)

        """Give Domain with URL"""
        parsed_uri = urlparse(self.start_urls[1])
        self.domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        print(self.domain)

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # the response containing a HTML form
    def parse(self, response):
        #extract data from every links
        links = self.le1.extract_links(response)
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
            if next_page:
                # print(next_page)
                next_page = self.domain + next_page
                yield response.follow(next_page, self.parse)
        except:
            print("there isn't other page")


    def AddIndex(self, Newindex):
        print (self.start_urls)
        self.start_urls.append(Newindex)
        print(self.start_urls)
        return self.start_urls

#Launch spider
if __name__ == "__main__":
    Scrap = WebScraping()
    Scrap.AddIndex("http://journals.plos.org/plosone/")

    """
    WebScrapping.AddIndex()
    process = CrawlerProcess()
    process.crawl(WebScrapping)
    process.start()
    """