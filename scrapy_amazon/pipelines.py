# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs

class ScrapyAmazonPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonCatePipeline(object):
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()
    def __init__(self):
        self.file = codecs.open('category.json', 'wb', encoding='utf-8') 

    
