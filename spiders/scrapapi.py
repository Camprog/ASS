import requests

"""
example requests : http://api.plos.org/search?q=title:"Drosophila" AND body:"RNA"&fl=id,abstract
field list : http://api.plos.org/solr/search-fields/

"""
class ScrapingApi():
    def __init__(self, url, keyword):
        self.url=url
        self.keyword=keyword

    def deep_request(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.url = self.url+"/search?q=everything:'"+self.keyword+"'"
            resp = requests.get(self.url)
            print (resp.text)

    def short_request(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.url = self.url + "/search?q=abstract:'" + self.keyword + "'"
            resp = requests.get(self.url)
            print(resp.text)


a=ScrapingApi('http://api.plos.org', 'agent-based' )
a.short_request()