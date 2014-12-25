import scrapy
from neiman_marcus.items import NeimanMarcusItem
from scrapy.http import Request
from urlparse import urljoin

#import selenium related
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 


class NeimanSpider(scrapy.Spider):
	name = "neiman"
	allowed_domains = ["www.neimanmarcus.com"]
	start_urls = ["http://www.neimanmarcus.com/Womens-Clothing/Categories/cat17740747_cat000001_cat000000/c.cat"]
	
	def __init__(self):
		self.driver = webdriver.Chrome("./chromedriver")
		self.driver.implicitly_wait(10)

	def __del__(self):
		self.driver.quit()
	def parse(self, response):
		items = []
		categories_url = response.xpath("//*[@class='category-menu']")[1].xpath("li/a/@href").extract()
		base_url = response.url
		for url in categories_url:
			self.log("in category")
			self.driver.get(urljoin(base_url,url))
			first_dress = self.driver.find_element_by_xpath("//li[@class='category-item'][1]/figure/figcaption/div[2]/a[@class='recordTextLink']")
			fd_url = first_dress.get_attribute("href")
			# yield Request(fd_url, callback=self.parse_item)
			self.driver.get(fd_url)
			items.append(self._get_item())
			next_url = self.driver.find_element_by_xpath("//a[@class='nextpage']")
			while (next_url.get_attribute("href") != ""):
				next_url.click()
				next_url = self.driver.find_element_by_xpath("//a[@class='nextpage']")
				item =self._get_item()
				items.append(item)
		return items
	
	def _get_item(self):
		item=NeimanMarcusItem()
		item["name"] = self.driver.find_element_by_xpath("//h1[@itemprop='name']").text
		item["description"] = self.driver.find_element_by_xpath("//*[@itemprop='description']").text
		self.log(item["name"], item["description"])
		return item

	# def parse_category(self, response):
	# 	self.log("in category")
	# 	self.driver.get(response.url)
	# 	first_dress = self.driver.find_element_by_xpath("//li[@class='category-item'][1]/figure/figcaption/div[2]/a[@class='recordTextLink']")
	# 	# item_urls = response.xpath("//li[@class='category-item'][1]/figure/figcaption/div[2]/a[@class='recordTextLink']/@href").extract()
	# 	base_url = response.url
	# 	item_urls = first_dress.get_attribute("href")
	# 	for url in item_urls:
	# 		yield Request(urljoin(base_url,url), callback=self.parse_item)

	def parse_item(self, response):
		self.log("in item")
		item = NeimanMarcusItem()
		self.driver.get(response.url)
		# next_page = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(By.CLASS_NAME, "nextpage"))
		next_url = self.driver.find_element_by_xpath("//a[@class='nextpage']").get_attribute("href")
		# next_url = next_page.get_attribute("href")
		self.log(next_url)

		item["name"] = response.xpath("//*[@itemprop='name']").extract()
		item["description"] = response.xpath("//*[@itemprop='description']").extract()
		item["price"] = 0
		item["url"] = response.url
		# item["sku_no"] = 
		# item["picture"] = 
		yield item
		if next_url != "":
			yield Request(urljoin(response.url,next_url), callback=self.parse_item)

