import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/'
    ]
    #self la instancia posterior de la case
    #response respuesta http de quotes
    def parse(self, response):
        with open('resultados.html','w',encoding='utf-8') as f:
            f.write(response.text)
