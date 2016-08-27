__author__ = 'aymon'

import scrapy
from math import ceil
import re
from urllib import quote_plus
from amznfrsh.items import GroceryItem
from scrapy.http import Request
from scrapy.selector import Selector

class AmazonSpider(scrapy.Spider):
    name = "amzn"
    allowed_domains = ["fresh.amazon.com"]
    start_urls = [
        "https://fresh.amazon.com/Gateway?browseZIP=20740&referer=Search%253Finput%253D%2526sort%253Dprice_low_to_high%2526browseNode%253D16310101%2526ref_%253Dgr_bb_s1%2526resultsPerPage%253D100"
    ]


    def start_requests(self):
        i = 1;
        yield Request('https://fresh.amazon.com/Gateway?browseZIP=20740&referer=Search%253Finput%253D%2526sort%253Dprice_low_to_high%2526pageNumber%253D{page}%2526browseNode%253D16310101%2526ref_%253Dgr_bb_s1%2526resultsPerPage%253D100'.format(page=i), callback=self.parse_category_level1)

    def parse_category_level1(self, response):
        selector = Selector(response)
        links = selector.xpath('//*[@id="div-categories"]/div/ul/li[2]/ul/li')
        for link in links:
            print link.xpath('a/@href')
            href = self.build_amzn_url(link.xpath('a/@href').extract()[0])
            yield Request(href, self.parse_category_level2)

    def parse_category_level2(self, response):
        selector = Selector(response)
        links = selector.xpath('//*[@id="div-categories"]/div/ul/li[3]/ul/li')
        for link in links:
            href = self.build_amzn_url(link.xpath('a/@href').extract()[0])
            print 'got to category level2: ' + selector.xpath('//*[@id="div-categories"]/div/ul/li[3]/ul/li/a/span[1]/text()').extract()[0];
            yield Request(href, self.parse_category_level3)

    def parse_category_level3(self, response):
        selector = Selector(response)
        href = selector.xpath('//*[@id="div-categories"]/div/ul/li[4]/a/@href').extract()[0]

        number_of_items = selector.xpath('//*[@id="searchSort"]/div[1]/text()').extract()[0]
        number_of_items = re.sub(r"\W", "", number_of_items)
        m = re.search('1.+?of(\d+)', number_of_items.strip(), re.MULTILINE)
        number_of_items = m.group(1)

        max_pages = ceil(float(number_of_items) / 100)

        href = href + '&pageNumber=1'
        href = self.build_amzn_url(href)
        href = re.sub('pageNumber%253D\d+', 'pageNumber%253D{page}', href)


        for i in range(1, int(max_pages) + 1):
            yield Request(href.format(page=i), callback=self.parse)


    def parse(self, response):
        for sel in response.xpath('//*[@id="searchResults"]/div[3]/div'):
            item = GroceryItem()
            try:
                title = sel.xpath('div/div[3]/div[3]/h4/input/@value').extract()[0].strip()
                price = re.sub(r"\$", "", sel.xpath('div/div[3]/div[3]/div/span/text()').extract()[0].strip())
                if len(price) > 0:
                    m = re.search('\$\d+\.\d+', str(price[0]))
                    if m is not None:
                        price = m.group(0)

                url = sel.xpath('div/div[3]/div[3]/h4/a/@href').extract()[0]
                img = sel.xpath('div/div[3]/div[2]/div/a/img/@src').extract()[0]
                category = sel.xpath('//*[@id="div-categories"]/div/ul/li[3]/a/span/text()').extract()[0].strip()
                print category
                category = category[2:]
                sub_category = sel.xpath('//*[@id="div-categories"]/div/ul/li[4]/a/span/text()').extract()[0].strip()
                print sub_category
                sub_category = sub_category[2:]
                #print img
                print title, price, url, category
                item['name'] = title
                item['category'] = category
                item['subcategory'] = sub_category
                item['url'] = url
                item['price'] = price
                item['image_url'] = img
                item['store_id'] = 2 # for the database, AmazonFresh is the second store.
                yield item
            except IndexError:
                continue


    def build_amzn_url(self, url):
        url = re.sub('https://fresh.amazon.com/','',url)
        return 'https://fresh.amazon.com/Gateway?browseZIP=20740&referer=' + quote_plus(quote_plus(url))
