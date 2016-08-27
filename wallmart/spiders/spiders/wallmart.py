import string
import urllib
import urlparse
from itertools import islice

from scrapy.http import Request, FormRequest
from scrapy.spiders import Spider
from scrapy.log import ERROR, WARNING, INFO, DEBUG

from spiders.items import ProductItem
from scrapy.selector import Selector

class WallmartSpider(Spider):
    name = 'walmart'
    allowed_domains = ["walmart.com"]
    start_urls = []

    SEARCH_URL = 'http://www.walmart.com/ip/={sku}'

    def __init__(self,
                 url_formatter=None
                 sku=None,
                 product_url = None,
                 *args, **kwargs):

        super(WallmartSpider, self).__init__(*args, **kwargs)

        if url_formatter is None:
            self.url_formatter = string.Formatter()
        else:
            self.url_formatter = url_formatter
            
        if sku is None and product_url is not None:
            self.SEARCH_URL = product_url
        if sku in not None and product_url is None:
            self.SEARCH_URL = self.SEARCH_URL.replace('{sku}',sku)

    def make_requests_from_url(self, _):
        """This method does not apply to this type of spider so it is overriden
        and "disabled" by making it raise an exception unconditionally.
        """
        raise AssertionError("Need a search term.")

    def start_requests(self):
        """Generate Requests from the SEARCH_URL and the search terms."""
        yield Request(
                self.url_formatter.format(
                    self.SEARCH_URL)
            )
        
    def parse(self, response):
        sel = Selector(response)

        item = ProductItem()
        item['name'] = sel.xpath('//div/h1/span/text()').extract()[0]
        item['price'] = sel.xpath('//div/["class"="js-price-display Price Price--stylized  Price--large hide-content display-inline-m price-display"]/text()').extract()[0]
        item['shipping_price'] = sel.xpath('//div/["class"=js-price-details-shipping pull-left offer-shipping-section js-offer-shipping-section offer-fulfillment-section hide-content display-block-m]/text()').extract()[0]
        item['quantity'] = sel.xpath('//div/["class"="chooser-option-current js-chooser-option-current active"]/text()').extract()[0]
        elements = {}
        rows = sel.select('//tr')
        for row in rows:
            values = row.select('td/text()').extract()
            elements[values[0]] = values[1]
        item['brand'] = elements['Brand:']
        item['manufacturer'] = elements['Manufacturer:']
        item['part_num'] = elements['Manufacturer Part Number:']
        item['description'] = sel('//section/["class"="product-about js-about-item"]/text()').extract()[0]

        yield item

    
