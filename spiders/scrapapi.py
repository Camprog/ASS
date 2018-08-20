import requests

"""
example requests : http://api.plos.org/search?q=title:"Drosophila" AND body:"RNA"&fl=id,abstract
field list : http://api.plos.org/solr/search-fields/
Science direct Key : 9b6fc59147caceaff0944b9259dec395
"""
class ScrapingApi():
    def __init__(self, api, keyword, feature):
        self.url=api
        self.keyword=keyword
        self.feature=feature

        if api == "plosone":
            self.url = 'http://api.plos.org'
            ScrapingApi.plosone()

        if api == "sciencedirect":
            self.url =
            ScrapingApi.science_direct()

    def plosone(self):
        if self.feature=="deep":
            response = requests.get(self.url)
            if response.status_code == 200:
                self.url = self.url+"/search?q=everything:'"+self.keyword+"'"
                resp = requests.get(self.url)
                print (resp.text)
        else:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.url = self.url + "/search?q=abstract:'" + self.keyword + "'"
                resp = requests.get(self.url)
                print(resp.text)

    def science_direct(self):
        

ScrapingApi("plosone", 'agent-based', "deep")
