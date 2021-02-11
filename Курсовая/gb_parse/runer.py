import os
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
#from gb_parse.spiders.autoyoula import AutoyoulaSpider
#from gb_parse.spiders.hhru import HhruSpider
#from gb_parse.spiders.instagram import InstagramSpider
#from gb_parse.spiders.zillow import ZillowSpider
#from gb_parse.spiders.instagram_handshake import InstagramHandshakeSpider


if __name__ == '__main__':
    load_dotenv(".env")
    tasks = []
    crawler_settings = Settings()
    crawler_settings.setmodule('gb_parse.settings')
    crawler_process = CrawlerProcess(settings=crawler_settings)
    #crawler_process.crawl(AutoyoulaSpider)
    #crawler_process.crawl(HhruSpider)
    #crawler_process.crawl(InstagramSpider, login=("+79160821910"), enc_password=("Tima19821308"), tag_list=["python", "питер", "программирование"],)
    #crawler_process.crawl(ZillowSpider)
    crawler_process.crawl(InstagramHandshakeSpider, login=("+79160821910"), enc_password=("Tima19821308"),)
    crawler_process.start()