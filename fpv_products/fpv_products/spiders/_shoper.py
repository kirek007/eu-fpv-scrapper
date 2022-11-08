import scrapy
import urllib.parse

from fpv_products.items import FpvItem


class ShoperSpider(scrapy.Spider):
    name = 'shoper'
    allowed_domains = [
        'znowodronach.pl',
        'tojalece.pl',
        'rcmaniak.pl'
    ]
    start_urls = [
        'https://znowodronach.pl/webapi/front/pl_PL/categories/37/products/PLN/?limit=40&page=1',
        'https://www.tojalece.pl/webapi/front/pl_PL/categories/79/products/PLN?limit=40&page=1',
        'https://www.rcmaniak.pl/webapi/front/pl_PL/categories/42/products/PLN?limit=40&page=1',  # Elektronika
        'https://www.rcmaniak.pl/webapi/front/pl_PL/categories/174/products/PLN?limit=40&page=1',  # FPV
        'https://www.rcmaniak.pl/webapi/front/pl_PL/categories/109/products/PLN?limit=40&page=1',  # Drony
    ]

    def parse(self, response, **kwargs):

        resp = response.json()
        list = resp["list"]
        url = response.request.url
        url_parts = urllib.parse.urlparse(url)

        for product in list:
            item = FpvItem()
            item["name"] = product["name"]
            item["shop"] = url_parts.netloc
            item["price"] = product["price"]["gross"]["base_float"]
            item["url"] = product["url"]
            item["can_buy"] = product["can_buy"]
            item["category"] = product["category"]["name"]
            item["producer"] = product["producer"]["name"] if "producer" in product else "None"

            yield item

        # Next page?

        query = dict(urllib.parse.parse_qsl(url_parts.query))
        current_page = int(query["page"])
        pages = int(resp["pages"])
        if current_page < pages:
            query.update({"page": str(current_page + 1)})
            next_url = url_parts._replace(query=urllib.parse.urlencode(query)).geturl()
            yield scrapy.Request(next_url)



