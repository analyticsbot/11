# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class WallmartItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    price = Field()
    shipping_price = Field()
    quantity = Field()
    brand = Field()
    manufacturer = Field()
    part_num = Field()
    description = Field()
