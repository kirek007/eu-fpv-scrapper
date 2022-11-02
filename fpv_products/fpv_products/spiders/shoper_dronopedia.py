import scrapy
import urllib.parse

from fpv_products.items import FpvItem


class ShoperSpider(scrapy.Spider):
    name = 'shoper_dronopedia'
    allowed_domains = [
        'dronopedia.pl'
    ]
    start_urls = [
        'https://www.dronopedia.pl/webapi/front/pl_PL/categories/tree/'

    ]
    ignore_category_id = [24, 54, 41, 31]

    def parse(self, response, **kwargs):
        resp = response.json()
        for category in resp:
            c_id = category["id"]
            if c_id in self.ignore_category_id:
                continue
            category_url = "https://dronopedia.pl/webapi/front/pl_PL/categories/%s/products/PLN/?limit=40&page=1" % c_id
            yield scrapy.Request(category_url, callback=self.parse_products)

    def parse_products(self, response, **kwargs):
        resp = response.json()
        list = resp["list"]

        for product in list:
            item = FpvItem()
            item["name"] = product["name"]
            item["price"] = product["price"]["gross"]["base_float"]
            item["url"] = product["url"]
            item["can_buy"] = product["can_buy"]
            item["category"] = product["category"]["name"]
            item["producer"] = product["producer"]["name"] if "producer" in product else "None"

            yield item

        # Next page?

        url = response.request.url
        url_parts = urllib.parse.urlparse(url)
        query = dict(urllib.parse.parse_qsl(url_parts.query))
        current_page = int(query["page"])
        pages = int(resp["pages"])
        if current_page < pages:
            query.update({"page": str(current_page + 1)})
            next_url = url_parts._replace(query=urllib.parse.urlencode(query)).geturl()
            yield scrapy.Request(next_url, callback=self.parse_products)


