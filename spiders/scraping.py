# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from urllib.parse import unquote
import requests
import scrapy
from scrapy import item
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.utils.project import get_project_settings
from scrapy.selector import HtmlXPathSelector, Selector

#import pywin32

class WebScraping(scrapy.Spider):
    #name of our spider
    name = "scraping"
    #list of url we want to scrap
    start_urls = ['http://jasss.soc.surrey.ac.uk/index_by_issue.html', 'https://www.comses.net/codebases']
    
    #rule to extract element in urls, allow to extract "page=xxx"
    le1 = LinkExtractor(canonicalize=True, unique=False)
    rules = [
        Rule(
            le1,
            follow=True,
            callback="parse_items"
        )
    ]
    
    list_urls = []
    #define if we want to search with keyword and article content
    def __init__(self, keyword, search):
        self.keyword = keyword
        self.search = search


    def start_requests(self):
        print(self.start_urls)
        self.items = dict()
        #if we want to choose which url we want to scrap, in this case we define directly url 0 (jasss)
        #url = str(input("Index, enter n° : "))
        url=0
        #define start_urls as url we want
        self.start_urls = self.start_urls[int(url)]

        """Give Domain with URL"""
        #parse start url to have our domain
        parsed_uri = urlparse(self.start_urls)
        self.domain = parsed_uri.netloc
        print("domain : ",self.domain)
        
        #return request
        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    # the response containing a HTML form
    def parse(self, response):
        # extract data from every links
        links = self.le1.extract_links(response)

        #in case of deep search
        if self.search == "deep":
            """Body of article content"""
            for link in links:
                print(link.url)
                #add url in empty list we created before
                WebScraping.list_urls.append(str(link.url))
            #launch class scraping_content after have list of urls list
            process.crawl(scraping_content)

        #in case of basic search
        else:
            #open file to put content inside
            file = open('content.txt', 'w')
            for link in links:
                #print(link.url, link.text)
                """ match URL with title and put them in a dict"""
                if self.keyword in link.text.lower():
                    #associate url to article title
                    self.items['url'] = str(link.title)
                    file.write(str(self.items['url']))

            file.close()
            
#after we created list of urls list we can scraping every link
class scraping_content(scrapy.Spider):
    #name of second spider
    name = "scraping_content"
    start_urls = WebScraping.list_urls
    items = []
    le1 = LinkExtractor(canonicalize=True, unique=False)
    rules = [
        Rule(
            le1,
            follow=True,
            callback="parse_items"
        )
    ]
    def start_requests(self):
        #content scraping on each url
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parsing)
        #open file to put data inside
        file = open('content.txt', 'w')
        
        #this part doesn't work, try to delete character we don't want but too many cases
        for i in self.items:
            i = i.replace(u'\xa0', u' ')
            i = i.replace(u'\r', u'')
            i = i.replace(u'\n ', u'')
            #encode ou decode?
            file.write(str(i.encode('utf-8')))
        file.close()
        
        
    def parsing(self, response):
        #different responses depends on website we want to analyze
        
        #self.item['keyword'] = str(response.xpath('//div[@id="keywords"]/a/text()').extract())
        #self.item['content'] = str(response.xpath('//body//p/text()').extract())
        
        #this one works on jasss article
        self.items.append(str(response.xpath('//body//p/text()').extract()))

#Launch spider
if __name__ == "__main__":
    #launch spider directly in script (usefull for windows environment)
    process = CrawlerProcess()
    """keyword to do a keyword search,search=deep to a deep search"""
    process.crawl(WebScraping, keyword="", search="deep")
    process.start()


# follow next page
#we have to include this part in script if we have index with many pages, it works for OpenABM
"""
try:
    #this response use css, only for comses.net /// Change page-item to adapt
    #next_page = response.css('li.page-item a::attr("href")').extract()[-1]

    a = input("Enter Class name : ")
    #a="xXx.button.button-primary.button-right"
    next_page_req = response.xpath('.//a[@class="' + a + '"]/@href').extract()[-1]
    print("page suivante : ", next_page_req)

    next_page = self.start_urls + next_page_req
    r = requests.get(next_page)

    if r.status_code != 200:
        next_page = "https://" + self.domain + next_page_req

        if requests.get(next_page).status_code != 200:
            next_page = next_page_req

            if requests.get(next_page).status_code != 200:
                next_page = "http://" + self.domain + next_page_req


    yield response.follow(next_page, self.parse)

except:
    print("there isn't other page")
"""
