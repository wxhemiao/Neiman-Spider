# -*- coding: utf-8 -*-
from neiman_marcus.postParser import MBProductManager
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NeimanMarcusPipeline(object):
    
    def __init__(self):
    	self.manager = MBProductManager()
    
    def process_item(self, item, spider):
        self.maneger.insertProductItem(item)
        return item
