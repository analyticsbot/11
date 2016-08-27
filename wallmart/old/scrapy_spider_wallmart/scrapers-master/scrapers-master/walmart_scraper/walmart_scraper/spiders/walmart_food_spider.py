from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from walmart_scraper.items import GroceryItem

class WalmartFoodSpider(Spider):
    name = "walmart_scraper"
    allowed_domains = ["www.walmart.com"]
    start_urls = ["http://www.walmart.com/cp/976759"]
    
    def parse(self, response):
      selector = Selector(response)
      links = selector.xpath('//div[@class="lhn-menu-flyout-inner lhn-menu-flyout-2col"]/ul[@class="block-list"]/li/a/@href|//div[@class="lhn-menu-flyout-inner lhn-menu-flyout-1col"]/ul[@class="block-list"]/li/a/@href')
      for link in links:
        href = link.extract()
        next_page = 'http://www.walmart.com' + href
        yield Request(next_page, callback=self.parse_page)


    def parse_page(self, response):
      selector = Selector(response)
      maxi = 1
      for i in range(1,9):
        xpath = '//ul[@class="paginator-list"]/li[{0}]/a/text()'.format(i)
        count = selector.xpath(xpath).extract()
        if count:
          maxi = int(count[0])
      for i in range (1,maxi):
        yield Request(response.url + '?page={0}'.format(i), callback=self.parse_item)

    def parse_item(self, response):
        selector = Selector(response)
        page = selector.xpath('//li[@class="tile-grid-unit-wrapper"]')
        for walmart_item in page:
          item = GroceryItem()
          price = walmart_item.xpath('.//div[@class="tile-price"]/div[@class="item-price-container"]/span[@class="price price-display"]/text()|.//div[@class="tile-price"]/div[@class="item-price-container"]/span[@class="price price-display price-not-available"]/text()').extract()+walmart_item.xpath('.//div[@class="tile-price"]/div[@class="item-price-container"]/span[@class="price price-display"]/span[@class="visuallyhidden"]/text()|.//div[@class="tile-price"]/div[@class="item-price-container"]/span[@class="price price-display price-not-available"]/span[@class="visuallyhidden"]/text()').extract()+walmart_item.xpath('.//div[@class="tile-price"]/div[@class="item-price-container"]/span[@class="price price-display"]/span[@class="sup"][2]/text()|.//div[@class="tile-price"]/div[@class="item-price-container"]/span[@class="price price-display price-not-available"]/span[@class="sup"][2]/text()').extract()
          if price:
            price = price[1] + price[3] + price[4];
          else:
            price = 0.00
          # iterate over deals
          item['name'] = walmart_item.xpath('.//a[@class="js-product-title"]/h3[@class="tile-heading"]/div/text()').extract()[0].strip()
          item['image_url'] = walmart_item.xpath('.//a[@class="js-product-image"]/img[@class="product-image"]/@src').extract()[0]
          item['price'] = price
          item['category'] = walmart_item.xpath('//nav[@id="breadcrumb-container"]/ol[@class="breadcrumb-list"]/li[@class="js-breadcrumb breadcrumb "][2]/a/text()').extract()[0].strip()
          item['subcategory'] = walmart_item.xpath('//nav[@id="breadcrumb-container"]/ol[@class="breadcrumb-list"]/li[@class="js-breadcrumb breadcrumb active"]/a/text()').extract()[0].strip()
          item['url'] = walmart_item.xpath('.//a[@class="js-product-image"]/@href').extract()[0]
          yield item