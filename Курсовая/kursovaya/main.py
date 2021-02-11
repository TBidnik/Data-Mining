import os
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from ..kursovaya.spiders.instagram_handshaker import InstagramSpider

if __name__ == "__main__":
    tasks = []
    crawler_settings = Settings()
    crawler_settings.setmodule("kursovaya.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(
        InstagramSpider,
        login=os.getenv("LOGIN"),
        enc_password=os.getenv("ENC_PASSWORD"),
        tag_list=["python", "питер", "программирование"],
    )
    crawler_process.start()