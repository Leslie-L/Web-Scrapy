import scrapy
#titulo =  //h1/a/text()
#citas = //span[@class="text" and @itemprop="text"]/text()
#top ten tags ='//div[contains(@class,"tags-box")]//span[@class="tag-item"]/a/text()'
#nex page = response.xpath('//li[@class="next"]/a/@href').get()
class QuotesSpider(scrapy.Spider):
    name='quote'
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]
    custom_settings={
        'FEED_URI':'quotes.json',
        'FEED_FORMAT':'json',
        #CUANTAS REQUEST PUEDE HACER A LA VEZ
        'CONCURRENT_REQUESTS':24,
        #LIMITE DE MEM RAM
        'MEMUSAGE_LIMIT_MB':2048,
        'MEMUSAGE_NOTIFY_MAIL':['mail@gmail.com'],
        'ROBOTSTXT_OBEY':True,
        'USER_AGENT':'NombrePeticion',
        'FEED_EXPORT_ENCODING': 'utf-8'
        

    }
    def parse_only_quotes(self,response,**kwargs):
        if kwargs:
            quotes= kwargs['quotes']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        next_page_button_link=response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes,cb_kwargs={'quotes':quotes})
        else:
            yield {
                'quotes':quotes
            }
    def parse(self,response):
        
        title = response.xpath('//h1/a/text()').get()
        citas = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top = response.xpath('//div[contains(@class,"tags-box")]//span[@class="tag-item"]/a/text()').getall()
        top_num= getattr(self,'top',None)
        if top_num:
            top_num = int(top_num)
            top=top[:top_num]

        
        yield {
            'title': title,
            'top_ten_tangs':top
        }
        
        next_page_button_link=response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes,cb_kwargs={'quotes':citas})

        
