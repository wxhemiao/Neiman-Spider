# -*- coding: utf-8 -*-

# Scrapy settings for neiman_marcus project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'neiman_marcus'

SPIDER_MODULES = ['neiman_marcus.spiders']
NEWSPIDER_MODULE = 'neiman_marcus.spiders'

DOWNLOADER_MIDDLEWARES = {
    # 'myproject.middlewares.CustomDownloaderMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    # 'neiman_marcus.WebkitDownloader': 543
}
# IMAGES_STORE = './img/'
# ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
ITEM_PIPELINES = {
	'neiman_marcus.pipelines.NeimanMarcusPipeline':100
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'neiman_marcus (+http://www.yourdomain.com)'
