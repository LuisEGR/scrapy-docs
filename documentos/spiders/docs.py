# -*- coding: utf-8 -*-
import os
import hashlib
from scrapy import Spider
from scrapy import Request
from scrapy import signals
from utilidades import Log
from bson.binary import Binary
from documentos.items import DocumentosItem

class DocsSpider(Spider):
    name = 'docs'

    def __init__(self, url='', tipos='', profindudad=3, * args, **kwargs):
        super().__init__(*args, **kwargs)
        domain = url.split("//")[-1].split("/")[0]
        Log.ok("Iniciando scrapping de: " + url)
        Log.ok("Dominio:" + domain)
        Log.ok("Tipos de archivo:" + tipos)
        Log.ok("Profundidad:" + str(profindudad))
        self.start_urls = [url]
        self.allowed_domains = [domain]
        self.allowed_extensions = tipos.split(',')
        self.profundidad_maxima = profindudad


    def parse(self, response):
        title = response.css('title::text').extract_first()
        path = response.url.replace(self.start_urls[0], '')
        links = response.css('a::attr(href)').extract()
        if 'paths' in response.meta:
            paths = response.meta['paths']
        else:
            paths = []

        paths.append({
            'TEXTO': title,
            'LINK': path
        })
        for link in links:            
            extension = link.split('.')[-1]
            urlfull = response.urljoin(link)
            if(extension in self.allowed_extensions):
                yield Request(urlfull, callback=self.guardar_archivo, meta={'title':title, 'paths': paths})
            else:
                if(response.meta['depth'] < self.profundidad_maxima):
                    yield Request(urlfull, meta={'paths': paths })

    def guardar_archivo(self, response):        
        filename = response.url.split('/')[-1]
        Log.msg("----------------------------")
        Log.msg("title:" + filename)
        Log.msg("url:" + response.url)
        Log.msg("sitio:" + self.allowed_domains[0])
        binary_file = Binary(response.body)
        m = hashlib.md5()
        m.update(binary_file)      
        hashmd5 = m.hexdigest()
        archivo = DocumentosItem()
        archivo['MD5'] = hashmd5
        archivo['SITE'] = self.allowed_domains[0]
        archivo['URL'] = response.url
        archivo['TITLE'] = filename
        archivo['ARCHIVO'] = binary_file
        archivo['PATH'] = response.meta['paths']
        yield archivo
