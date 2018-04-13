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
        print(self.allowed_extensions)
        self.profundidad_maxima = profindudad


    def parse(self, response):
        Log.log(response.url)
        if not b'text/html' in response.headers['Content-Type']:
          print("Ignorado: ", response.headers['Content-Type'])
          return False
        links_texts = []
        links = []
        all_links = response.css('a')
        for link in all_links:
          if link.css('::attr(href)').extract_first():
            links_texts.append(link.css('*::text').extract_first())
            links.append(link.css('::attr(href)').extract_first())

        if 'paths' in response.meta:
          paths = response.meta['paths']
        else:
          paths = [] 
        print(len(links), '_', len(links_texts))
        for _link, _link_text in zip(links, links_texts):       
          pat_aux = paths[:]
          pat_aux.append({
            'TEXTO': _link_text,
            'LINK': _link
          })
          extension = _link.split('.')[-1]
          urlfull = response.urljoin(_link)
          if(extension in self.allowed_extensions):
              yield Request(urlfull, callback=self.guardar_archivo, meta={'paths': pat_aux})
          else:
              if(response.meta['depth'] < self.profundidad_maxima):
                  yield Request(urlfull, callback=self.parse,  meta={'paths': pat_aux})


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
