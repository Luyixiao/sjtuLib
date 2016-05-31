# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json  
import codecs  
  
  
class appstorePipeline(object):  
    def __init__(self):  
        self.file = codecs.open('appstore.json', 'wb', encoding='utf-8')  
  
    def process_item(self, item, spider):  
        line = json.dumps(item['name']) +","+json.dumps(item['status'])+ '\n'  
        self.file.write(line.decode("unicode_escape"))  
        return item  
