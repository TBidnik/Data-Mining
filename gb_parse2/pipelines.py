# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import pymongo
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GbParse2Pipeline:
    def process_item(self, item, spider):
        return item


class MongoSavePipeline:
    def __init__(self):
        self.db_client = pymongo.MongoClient(os.getenv('DATE_BASE'))

    def process_item(self, item, spider):
        db = self.db_client['gb_parse2']
        collection = db[spider.name]
        collection = db[type(item).__name__]
        collection.insert_one(item)
        return item


class GbImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url in item.get("images", []):
            yield Request(img_url)

    def item_completed(self, results, item, info):
        item['images'] = [itm[1] for itm in results]
        return item