# -*- coding: utf-8 -*-
"""
Created on Thu May  2 10:28:59 2019

@author: Guanglin Kuang
"""

import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "phrase"

    phrase = ''

    def start_requests(self):
        url = 'https://en.bab.la/dictionary/swedish-english/'
        phrase_q = getattr(self, 'phrase', None)

        if phrase_q is not None:
            url = url + phrase_q
            if '-' in phrase_q:
                self.phrase = ' '.join(phrase_q.split('-'))
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        entry_path = response.xpath(".//div[@class='content']/div[@class='quick-results container']/div[@class='quick-result-entry']/div[@class='quick-result-overview']/ul[@class='sense-group-results']/li")
        trans_path = entry_path.xpath(".//a[contains(@title, 'in Swedish')]/text()")

        trans = trans_path.getall()[0:2]

        yield {
            'phrase': self.phrase,
            'trans': trans,
        }
