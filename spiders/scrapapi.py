# -*- coding: utf-8 -*-
import requests
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json

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
            self.url = "https://api.elsevier.com/authenticate/"
            ScrapingApi.science_direct(self)

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
        payload={'APIKey': "9b6fc59147caceaff0944b9259dec395"}
        response=requests.get("http://api.elsevier.com/content/search/scopus?query=KEY%28agent-based%29", payload)

        ## Load configuration
        con_file = open("config.json")
        config = json.load(con_file)
        con_file.close()

        ## Initialize client
        client = ElsClient(config['apikey'])

        ## ScienceDirect (full-text) document example using PII
        pii_doc = FullDoc(sd_pii='S1674927814000082')
        if pii_doc.read(client):
            print("pii_doc.title: ", pii_doc.data)
            pii_doc.write()
        else:
            print("Read document failed.")

        ## ScienceDirect (full-text) document example using DOI
        doi_doc = FullDoc(doi='10.1016/S1525-1578(10)60571-5')
        if doi_doc.read(client):
            print("doi_doc.title: ", doi_doc.data)
            doi_doc.write()
        else:
            print("Read document failed.")



ScrapingApi("sciencedirect", 'agent-based', "deep")
