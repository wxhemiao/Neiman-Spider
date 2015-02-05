from postParser import MBProductManager

	
class MBParserTestUnit(object):
	def __init__:
		crawlItems = []

	def newCrawlItemWithValues(supl_ID, cat_ID, dsn, name, sku, orig, curr, desc, dsn_desc, url, img_url):
		newItem = {}
		newItem['supplierID'] = supl_ID #Always constant
		newItem['categoryID'] = cat_ID
		newItem['designer'] = dsn  #good_name, good_designer
		newItem['name'] = name #nick_name
		newItem['sku'] = sku
		newItem['orig_price'] = orig
		newItem['curr_price'] = curr
		newItem['description'] = desc
		newItem['designer_desc'] = dsn_desc
		newItem['url'] = url
		newItem['image_urls'] = img_url
		return newItem
	def loadCrawlItemsFromJSON(path):

	def DoTest:
		productManager = MBProductManager()
		for aProduct in crawlItems:
			productManager.insertProductItem(aProduct)
			

def main():
	print 'Test unit for MBParser has started.'

if __name__ == "__main__":
	main()
else:
	print 'You have mistakenly called this test unit as a module. Terminating.'
	raise NameError('Test unit must be executed as program.')