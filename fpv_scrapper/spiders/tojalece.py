import scrapy
import sqlite3

class ToJaLeceSpider(scrapy.Spider):
  name = 'tojalece_silniki'
  start_urls = ['https://www.tojalece.pl/drony/wyscigowe/silniki/bezszczotkowe/1/default/1/f_availability_2/1']

  def parse(self, response):
    for art in response.css('div.product-inner-wrap'):
      availability = "Dostepny"
      yield {
        'title': art.css('span.productname::text').get(), 
        'price': art.css('div.price > em::text').get(),
        'availability' : availability,
        'quantity' : 'n/a',
        }