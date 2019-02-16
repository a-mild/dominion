# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 00:39:33 2018

@author: Alex
"""

import scrapy


class DominionSpider(scrapy.Spider):
    name = "dominion"
    start_urls = ["https://dominion.games/"]


    def parse(self, response):
        return
#        return scrapy.FormRequest.from_response(
#                response,
#                formdata={"username": "schlafi", "password": "Ganxta89"},
#                callback=self.after_login)
        
#    def after_login(self, response):
#        print(response.css("title"))
#        return