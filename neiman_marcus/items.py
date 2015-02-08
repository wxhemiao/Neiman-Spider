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
	purchase_link = scrapy.Field()
	designer = scrapy.Field()
	price = scrapy.Field()
	discount_price = scrapy.Field()
	url = scrapy.Field()
	sku = scrapy.Field()
	image_urls = scrapy.Field()
	images = scrapy.Field()
	# picture = scrapy.Field()

class MBRawCrawlItem(scrapy.Item):
	supplierID = scrapy.Field()  #Always constant
	categoryID = scrapy.Field()
	designer = scrapy.Field()  #good_name, good_designer
	name = scrapy.Field() #nick_name
	sku = scrapy.Field()
	orig_price = scrapy.Field()
	curr_price = scrapy.Field()
	description = scrapy.Field()
	designer_desc = scrapy.Field()
	url = scrapy.Field()
	image_urls = scrapy.Field()

