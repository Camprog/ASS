# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from nltk.corpus import stopwords
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import nltk
import io

import numpy

from scrapy.utils.project import get_project_settings
from scrapy.selector import HtmlXPathSelector

#https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# import pywin32
# CD .\spiders
# scrapy runspider scraping.py

class WebScraping(scrapy.Spider):
    name = "scraping"
    start_urls = ['http://jasss.soc.surrey.ac.uk/index_by_issue.html', 'https://www.comses.net/codebases']

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
        self.search = search


    def start_requests(self):
        print(self.start_urls)
        self.items = dict()
        url = str(input("Index, enter n° : "))
        self.start_urls = self.start_urls[int(url)]

        """Give Domain with URL"""
        parsed_uri = urlparse(self.start_urls)
        self.domain = parsed_uri.netloc
        print("domain : ",self.domain)

        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    # the response containing a HTML form
    def parse(self, response):
        # extract data from every links
        links = self.le1.extract_links(response)

        for link in links:
            self.items[link] = str(response.xpath('//body//p//text()').extract())

        #deep search
        if self.search == "deep":
            stopWords = set(stopwords.words('english'))
            print(stopWords)
            file = open('content.txt', 'w')

            """Body of article content"""
            for link in links:
                self.items[link] = str(response.xpath('//body//p/text()').extract())
                content=str(response.xpath('//body//p/text()').extract())
                content = content.replace(u'\xa0', u' ')
                file.write(str(content.encode('utf-8')))
            file.close()

        #basic search
        else:
            file = open('content.txt', 'w')
            for link in links:
                #print(link.url, link.text)
                """ match URL with title and put them in a dict"""
                if self.keyword in link.text.lower():
                    self.items[link.url] = str(link.title)
                    file.write(str(self.items[link.url]))

            file.close()

        # follow next page
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
#Launch spider
if __name__ == "__main__":
    process = CrawlerProcess()
    """keyword to do a keyword search,search=deep to a deep search"""
    process.crawl(WebScraping, keyword="", search="deep")
    process.start()
