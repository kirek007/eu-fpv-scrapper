import scrapy
import urllib.parse

from fpv_products.items import FpvItem


class ShoperSpider(scrapy.Spider):
    name = 'shoper'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.categories_endpoint = 'webapi/front/pl_PL/categories/tree/'

        self.sites_config = {
            'znowodronach.pl': {
                'ignored_categories': [],
            },
            'tojalece.pl': {
                'ignored_categories': [],
            },
            'rcmaniak.pl': {
                'ignored_categories': [],
            },
            'dronopedia.pl': {
                'ignored_categories': [],
            },
        }

        self.allowed_domains = self.sites_config.keys()
        self.start_urls = ['https://%s/%s' % (domain, self.categories_endpoint) for domain in self.sites_config.keys()]

    def _site_config(self, url):
        url_parts = urllib.parse.urlparse(url)
        return self.sites_config[url_parts.netloc]

    @staticmethod
    def _get_category_url(url, category_id):
        url_parts = urllib.parse.urlparse(url)
        return "https://%s/webapi/front/pl_PL/categories/%s/products/PLN/?limit=40&page=1" % (
        url_parts.netloc, category_id)

    def parse(self, response, **kwargs):
        resp = response.json()
        ignored_categories = self._site_config(response.request.url)['ignored_categories']

        for category in resp:
            c_id = category["id"]
            if c_id in ignored_categories:
                continue
            category_url = self._get_category_url(response.request.url, c_id)
            yield scrapy.Request(category_url, callback=self.parse_products)

    def parse_products(self, response, **kwargs):
        resp = response.json()
        all_items = resp["list"]
        url = response.request.url
        url_parts = urllib.parse.urlparse(url)

        for product in all_items:
            item = FpvItem()
            item["name"] = product["name"]
            item["shop"] = url_parts.netloc
            item["price"] = product["price"]["gross"]["base_float"]
            item["url"] = product["url"]
            item["can_buy"] = product["can_buy"]
            item["category"] = product["category"]["name"]
            item["category_id"] = product["category"]["id"]
            item["producer"] = product["producer"]["name"] if "producer" in product else "None"
            item["image"] = "https://%s/environment/cache/images/120_120_productGfx_%s.jpg" % (url_parts.netloc, product["main_image"])

            yield item

        # Next page?

        query = dict(urllib.parse.parse_qsl(url_parts.query))
        current_page = int(query["page"])
        pages = int(resp["pages"])
        if current_page < pages:
            query.update({"page": str(current_page + 1)})
            next_url = url_parts._replace(query=urllib.parse.urlencode(query)).geturl()
            yield scrapy.Request(next_url, callback=self.parse_products)
