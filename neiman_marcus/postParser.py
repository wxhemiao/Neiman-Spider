import md5
import random
import MySQLdb
import string

def randomStringOfSize(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def md5_digest(s):
    digest = md5.new()
    digest.update(s)
    return digest.hexdigest()

def generateIDForProduct(item):
    mDigest = md5.new()
    mDigest.update(randomStringOfSize(32))
    mDigest.update(item["name"])
    mDigest.update(item["url"])
    mDigest.update(item["description"])
    return mDigest.hexdigest()

def generateSetIDForProduct(item):
    return md5_digest(item['name']+randomStringOfSize(32))

def generateDesignerIDForProduct(item):
    return md5_digest(item['designer']+randomStringOfSize(32)+item['designer_desc'])

def newSetForProduct(item, len):
    return {'ID':generateSetIDForProduct(item), 'usage':'product_picture', 'good_id':item['good_id'], 'count':item['imageurls'].length, 'name':item['name']}

def newImageWithURL(url, setid, Imgindex):
    aImage = {}
    aImage['ID'] = md5_digest(randomStringOfSize(32)+url)
    aImage['extURL'] = url
    aImage['index'] = Imgindex
    aImage['URL'] = 'http://image.myblaire.com/'+aImage['ID'] + '.' + url[url.rfind('.'):]
    return aImage

class MBImageManager(object):
    def __init__ (self):
        self.sets  = []
        self.assets = []
    def newSetIDWithImagesFor(self,item, imageurls):
        aSet = newSetForProduct(item), imageurls.length()
        self.sets.append(aSet)
        i = 0
        for aImageURL in imageurls:
            self.assets.append(newImageWithURL(aImageURL, aSet['ID'], i))
            i += 1
    def collateShellScriptTo(self,path):
        shFile = open(path, "w")
        for imageItem in self.assets:
            imgURL = imageItem['URL']
            shFile.write(u'wget {0:s} -O {1:s} \n'.format(imageItem['extURL'], imgURL[imgURL.rfind('/'):]))
        shFile.close()

#Processors for item information

class MBProductManager(object):
    def __init__(self):
        self.goods = []
        self.designers = []
        self.imageManager = MBImageManager()
        #Load existing designers on board
        self.conn = MySQLdb.connect('127.0.0.1', 'jimmy', '19960223', 'mibao')
        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.cursor.execute('select designer_id as ID, designer_name as name, designer_desc as description from t_designer')
        self.designers = [item for item in self.cursor.fetchall()]
    def designerIDForItem(self,item):
        for x in self.designers:
            if item.designer.upper() == x['name'].upper():
                return x['ID']
            else:
                newDesigner = {}
                newDesigner['ID'] = generateDesignerIDForProduct(item)
                newDesigner['description'] = item.designer_desc
                newDesigner['name'] = item.designer_name
                self.designers.append(newDesigner)
                return newDesigner['ID']
    def insertProductItem(self,item):
        newItem = {}
        newItem['good_id'] = generateIDForProduct(item)
        newItem['good_sku'] = item['sku']
        newItem['supplier_id'] = item['supplierID']
        newItem['category_id'] = item['categoryID']
        newItem['designer_id'] = self.designerIDForItem['designer']
        newItem['good_designer'] = item['designer']
        newItem['name'] = item['name']
        newItem['cur_price'] = item['curr_price']
        newItem['orig_price'] = item['orig_price']
        newItem['discount'] = newItem['cur_price']/newItem['orig_price']
        newItem['description'] = item['description']
        newItem['url'] = item['url']
        imgSID = self.imageManager.newSetIDWithImagesFor(item, item['image_urls'])
        newItem['imageSet'] = imgSID
    def commitProducts(self):
        sqlQuery = """insert into t_goods (good_id, good_sku, supplier_id, designer_id, good_designer, good_name, nick_name, 
                original_price, current_price, category_id, """

