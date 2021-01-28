
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse2.spiders.autoyoula import AutoyoulaSpider
from gb_parse2.spiders.hhru import HHruSpider
from gb_parse2.spiders.instagram import InstagramSpider
from gb_parse2.spiders.zillow import ZillowSpider


if __name__ == "__main__":
    tasks = []
    crawler_settings = Settings()
    crawler_settings.setmodule('gb_parse2.settings')
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(AutoyoulaSpider)
    crawler_process.crawl(HHruSpider)
    crawler_process.crawl(InstagramSpider, tag_list=['python', 'питер', 'программирование'])
    crawler_process.crawl(ZillowSpider)
    crawler_process.start()