import scrapy
import sqlite3

class RcmaniakSpider(scrapy.Spider):
  name = 'rcmaniak_silniki'
  start_urls = ['https://rcmaniak.pl/pl/c/Silniki/113']
  
  def parse(self, response):
    for art in response.css('div.product-inner-wrap'):
      yield {
        'title': art.css('span.productname::text').get(), 
        'price': art.css('div.price > em::text').get(),
        'availability' :  print('Dostepny') if art.css('button.addtobasket').get() else print('Nie dostepny'),
        'quantity' : 'n/a',
        }
        
    next_page = ""
    try:
      next_page = response.css('li.last > a').attrib["href"]
    except:
      pass
    if next_page:
      next_page_url = "https://rcmaniak.pl" + next_page
      yield scrapy.Request(next_page_url, callback=self.parse)

