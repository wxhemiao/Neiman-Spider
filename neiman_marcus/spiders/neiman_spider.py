import scrapy
from neiman_marcus.items import NeimanMarcusItem
from scrapy.http import Request
from urlparse import urljoin

#import selenium related
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

from lxml import etree
import time
import re

class NeimanSpider(scrapy.Spider):
	name = "neiman"
	allowed_domains = ["www.neimanmarcus.com/en-us"]
	# start_urls = ["http://www.neimanmarcus.com/Womens-Clothing/Categories/cat17740747_cat000001_cat000000/c.cat"]
	
	def __init__(self):
		self.driver = webdriver.Chrome("./chromedriver")
		self.driver.implicitly_wait(30)
		category_urls = []
		self.start_urls = ["http://www.neimanmarcus.com/en-us/Totes/cat40860745_cat42110769_cat13030735/c.cat"]
		
		# append all items URLs before parsing
		self.driver.get(self.start_urls[0]) #start from the first page
		time.sleep(15)
		close_button = self.driver.find_element_by_id("closeButton")
		close_button.click()
		
		page_source = self.driver.page_source
		urls = self.get_item_urls(page_source)
		self.start_urls.extend(urls)

		next_page = self.driver.find_element_by_xpath("//a[@id='paging_next']")
		total_pages = int(self.driver.find_element_by_xpath("//*[@id='epagingBottom']/li[7]").get_attribute("pagenum"))
		print total_pages
		# next_url = next_page.get_attribute("href")
		for page in xrange(2):
			print page
			time.sleep(5)
			next_page.click()
			time.sleep(2)
			self.start_urls.extend(self.get_item_urls(self.driver.page_source))
			next_page = self.driver.find_element_by_xpath("//a[@id='paging_next']")
	
	def __del__(self):
		self.driver.close()
		pass

	def get_item_urls(self,page_source):
		tree = etree.HTML(self.driver.page_source)
		item_urls = tree.xpath("//li[@class='category-item']/figure/figcaption/div[2]/a[@class='recordTextLink']/@href")
		item_urls = ["http://www.neimanmarcus.com/en-us"+url for url in item_urls]
		return item_urls


	def parse(self, response):
		yield self.parse_item(response)

	def parse_item(self, response):
		item=NeimanMarcusItem()
		product_name = "".join(response.xpath("//h1[@itemprop='name']/text()").extract())
		item["name"] = re.sub("\s+", " ", product_name)
		item["purchase_link"] = response.url
		item["description"] = response.xpath("//*[@class='product-details-info']").extract()
		
		# check if there is a discount
		adorn_price = response.xpath("//*[@class='price-adornments']/text()").extract()
		if len(adorn_price) != 0:
			item["price"] = parse_price(adorn_price[0])
			item["discount_price"] = parse_price(response.xpath("//*[@itemprop='price']/text()").extract()[0])
		else:
			item["price"] = parse_price(response.xpath("//*[@itemprop='price']/text()").extract()[0])
			item["discount_price"] = item["price"]
		
		item["sku"] = response.xpath("//small/text()").extract()[0]
		item["image_urls"] = response.xpath("//ul[@class='list-inline']/li/img/@data-zoom-url").extract()



		# self.log(item["name"], item["sku"])
		return item

def parse_price(price):
	return float(re.match("\$[0-9,.,\,]*",price).group(0).replace("$","").replace(",",""))

