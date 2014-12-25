# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NeimanMarcusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	name = scrapy.Field()
	description = scrapy.Field()
	price = scrapy.Field()
	url = scrapy.Field()
	# sku_no = scrapy.Field()
	# picture = scrapy.Field()	