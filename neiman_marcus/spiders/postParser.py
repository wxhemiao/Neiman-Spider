import md5
class Image_Asset(object):
	def __init__ (self, asset_id = None, index = None, url = None, name = None, target_name = None):
		self.asset_id = asset_id
		self.index = index
		self.url = url
		self.name = name
		self.target_name = target_name
#pragma end

class Image_Set(object):
	def __init__ (self, set_id = None, good_id = None, count = 0):
		self.set_id = set_id
		self.good_id = good_id
		self.count = count
#pragma end

def generate_id_for_product(item):
	mDigest = md5.new()
	mDigest.update(item["name"])
	mDigest.update(item["purchase_link"])
	mDigest.update(item["description"])
	return mDigest.hexdigest()
#pragma end

def collateImageItems(urls, good_id):
	Counter = 0
	# Construct Dictionary
	resDic = {'Assets': None, 'Set': None, 'Shell':''}
	for aImage in urls:
		Counter = Counter + 1
		mDigest = md5.new()
		mDigest.update(aImage)
		mDigest.update(good_id)
		MD5Digest = mDigest.hexdigest
		imageName = aImage[aImage.rfind('\\')+1:]
		targetName =  MD5Digest+aImage[aImage.rfind('.')+1:]
		resDic['Assets'].append(Image_Asset(MD5Digest, Counter, aImage, imageName, targetName))
		resDic['Shell'].append('wget %s -O %s \n' % aImage, targetName)
	mDigest = md5.new()
	for aImage in urls:
		mDigest.update(aImage)
	setid = mDigest.hexdigest
	resDic['Set'] = Image_Set(setid, good_id, urls.length)
	return resDic