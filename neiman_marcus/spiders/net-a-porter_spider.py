import scrapy
from neiman_marcus.items import MBRawCrawlItem
from scrapy.http import Request
from urlparse import urljoin

#import selenium APIs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from lxml import etree
import time
import re

class NetAPorterSpider(scrapy.Spider):
	name = "net-a-porter"
	allowed_domains = ["www.net-a-porter.com/"]
	# start_urls = ["http://www.neimanmarcus.com/Womens-Clothing/Categories/cat17740747_cat000001_cat000000/c.cat"]
	
	def __init__(self):
		self.driver = webdriver.Chrome("./chromedriver")
		# self.driver.implicitly_wait(30)
		category_urls = []
		self.start_urls = ["http://www.net-a-porter.com/sg/en/Shop/Bags/All?cm_sp=topnav-_-bags-_-allbags&pn=1&image_view=product&dScroll=0&npp=view_all"]
		
		# append all items URLs before parsing
		self.driver.get(self.start_urls[0]) #start from the first page

		# time.sleep(15)

		
		#get item URLs of the first page
		time.sleep(1)
		page_source = self.driver.page_source
		urls = self.get_item_urls(page_source)
		self.start_urls.extend(urls)
		time.sleep(5)
		
	def __del__(self):
		self.driver.close()
		pass
	def get_item_urls(self,page_source):
		tree = etree.HTML(self.driver.page_source)
		item_urls = tree.xpath("//*[@id='product-list']/div[@class='product-details']/div[@class='description']/a/@href")
		item_urls = ["http://www.net-a-porter.com/sg/en"+url for url in item_urls]
		return item_urls


	def parse(self, response):
		yield self.parse_item(response)

	def parse_item(self, response):
		item = MBRawCrawlItem()
		# item["supplierID"] = scrapy.Field()  #Always constant
		# item["categoryID"] = scrapy.Field()
		item["designer"] = response.xpath("//h2[@itemprop='brand']/text()").extract() #good_name, good_designer
		item["name"] = response.xpath("//h1[@itemprop='name']/text()").extract() #nick_name
		sku = response.xpath("//*[@id='product-details-container']/div[3]/p")
		#TODO
		
		item["sku"] = re.match("\d{6}",sku).group(0)
		item["orig_price"] = scrapy.Field()
		item["curr_price"] = parse_price(response.xpath("//*[@itemprop='price']/text()").extract())
		item["description"] = response.xpath("//*[@id='editors-notes-content']/li/div").extract()
		# item["designer_desc"] = scrapy.Field()
		
		item["url"] = response.url
		# parse the img urls
		images = response.xpath("//img[@class='imgThumbnails']/@src").extract()
		images = [img.replace("//","").replace("xs","xl") for img in images]
		item["image_urls"] = response.xpath("//img[@class='imgThumbnails']/@src").extract()


		# self.log(item["name"], item["sku"])
		return item

def parse_price(price):
	'''convert the price in string to int, in USD'''
	return float(re.match("\$[0-9,.,\,]*",price).group(0).replace("$","").replace(",",""))
def parse_sku(sku):
	pass
