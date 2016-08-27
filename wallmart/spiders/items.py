# -*- coding: utf-8 -*-
from scrapy import Item, Field


class ProductItem(Item):
    # define the fields for your item here like:
    keyword = Field()
    total_matches = Field()
    all_brands = Field()

    name = Field()
    price = Field()
    shipping_price = Field()
    quantity = Field()
    brand = Field()
    manufacturer = Field()
    part_num = Field()
    description = Field()
