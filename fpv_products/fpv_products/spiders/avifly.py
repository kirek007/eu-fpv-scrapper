import json
import urllib
import scrapy

from fpv_products.items import FpvItem


class AviSpider(scrapy.Spider):
    name = 'avifly'
    start_urls = ['https://avifly.pl/pl/']

    def parse(self, response):
        categories = response.css('li.mm_has_sub ')[0].css('div.ets_mm_block_content > a')
        for c in categories:
            link = c.attrib['href']
            yield scrapy.Request(link, callback=self.parse_category)
            break

    def parse_category(self, response):
        products = response.css('div.products-list__content > article.product-miniature > a')
        for p in products:
            link = p.attrib['href']
            yield scrapy.Request(link, callback=self.parse_product)

        next_page = response.css("nav.pagination > ul > li > a.next")
        if next_page:
            yield scrapy.Request(next_page.attrib["href"], callback=self.parse_category)

    def parse_product(self, response):
        url = response.request.url
        url_parts = urllib.parse.urlparse(url)
        data = json.loads(response.css('#product-details').attrib["data-product"])

        item = FpvItem()
        item["name"] = data["name"]
        item["shop"] = url_parts.netloc
        item["price"] = data["price_amount"]
        item["url"] = response.request.url
        item["can_buy"] = data["availability"] == "available"
        item["category"] = data["category_name"]
        item["category_id"] = data["category"]
        item["producer"] = response.css("div.manufacturer > div > a::text").get()
        item["image"] = data["images"][0]["bySize"]["cart_default"]["url"]

        yield item
