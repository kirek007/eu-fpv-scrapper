import scrapy
import sqlite3


class AviSpider(scrapy.Spider):
    name = 'avi_silniki'
    start_urls = ['https://avifly.pl/pl/silniki-do-dronow/?q=Dost%C4%99pno%C5%9B%C4%87-W+magazynie']

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
        for art in response.css('.product-miniature'):
            item = art.css('a.product-thumbnail').attrib['href']
            yield scrapy.Request(item, callback=self.parse_item)

    def parse_item(self, response):
        yield {
            'title': response.css('div.product-information > h1::text').get(),
            'price': response.css('p.product-price > span::text').get(),
            'availability': response.css('div.availability > div > span::text').get(),
            'quantity': response.css('div.quantity > div > span::text').get(),
        }
