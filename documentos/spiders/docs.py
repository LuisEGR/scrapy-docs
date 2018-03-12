# -*- coding: utf-8 -*-
import os
from scrapy import Spider
from scrapy import Request
from scrapy import signals
from utilidades import save_pdf
from utilidades import Log
from utilidades import delete_temporal_files

class DocsSpider(Spider):
    name = 'docs'
    allowed_domains = ['poderjudicialags.gob.mx']
    start_urls = ['http://www.poderjudicialags.gob.mx/']
    allowed_extensions = ['pdf']
    profundidad_maxima = 3

    def parse(self, response):
        links = response.css('a::attr(href)').extract()
        for link in links:
            extension = link.split('.')[-1]
            urlfull = response.urljoin(link)
            if(extension in self.allowed_extensions):
                yield Request(urlfull, callback=self.guardar_pdf)
            else:
                if(response.meta['depth'] < self.profundidad_maxima):
                    yield Request(urlfull)

    def guardar_pdf(self, response):
        filename = response.url.split('/')[-1]
        save_pdf(response, filename, "./files/")
