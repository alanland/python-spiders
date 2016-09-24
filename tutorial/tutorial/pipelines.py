# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import codecs
import json


class JsonWithEncodingTencentPipeline(object):
    def __init__(self):
        self.file = codecs.open('tencent.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def process2(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)

    def spider_closed(self, spider):
        self.file.close()


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = codecs.open('tencent.jl', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item


from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item


from pymongo import MongoClient


class MongoPipline(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.spider_data
        self.collection = self.db.tencentHr

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
