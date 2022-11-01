import scrapy
import sqlite3

class NobshopSpider(scrapy.Spider):
  name = 'nobshop_silniki'
  start_urls = ['https://www.nobshop.pl/silniki-bezszczotkowe-do-dronow-wyscigowych-c-62.html']
  
  # def __init__(self):

  #   self.con = sqlite3.connect('silniki.db')
  #   self.cur = self.con.cursor()
  #   self.cur.execute("""
  #     CREATE TABLE IF NOT EXISTS motor(
  #         shop TEXT,
  #         title TEXT,
  #         price TEXT
  #     )
  #     """)
  def parse(self, response):
    for art in response.css('.ProdCena'):
      availability = "n/a"
      try:
        availability = str.strip(art.css('ul > li:nth-child(2) > b::text').get())
      except:
        pass
      yield {
        'title': art.css('h3 > a::text').get(), 
        'price': art.css('span.Cena::text').get(),
        'availability' : availability,
        'quantity' : 'n/a',
        }

    current_page = response.css('div.IndexStron > a.Aktywna::text').get()
    next_page = int(current_page) + 1
    next_page_url = "https://www.nobshop.pl/silniki-bezszczotkowe-do-dronow-wyscigowych-c-62.html/s=" + str(next_page)
    print()
    yield scrapy.Request(next_page_url, callback=self.parse)

