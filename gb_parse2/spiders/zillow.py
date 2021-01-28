from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import scrapy


class ZillowSpider(scrapy.Spider):
    name = "zillow"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.zillow.com/san-francisco-ca/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.browser = webdriver.Firefox()

    def parse(self, response):
        for pag_url in response.xpath(
            '//nav[@aria-label="Pagination"]//a[contains(@class, "Pagination")]/@href'
        ):
            yield response.follow(pag_url, callback=self.parse)
        for ads_url in response.xpath(
            '//article[@role="presentation"]//a[contains(@class, "list-card-link")]/@href'
        ):
            yield response.follow(ads_url, callback=self.ads_parse)

    def ads_parse(self, response):
        self.browser.get(response.url)
        media_col = self.browser.find_element_by_xpath('//div[contains(@class, "ds-media-col")]')
        len_photos = len(
            media_col.find_elements_by_xpath('//picture[contains(@class, "media-stream-photo")]')
        )
        while True:
            for _ in range(5):
                media_col.send_keys(Keys.PAGE_DOWN)
            photos = media_col.find_elements_by_xpath(
                '//picture[contains(@class, "media-stream-photo")]'
            )
            len_photos_tmp = len(photos)
            if len_photos_tmp == len_photos:
                break
            len_photos = len_photos_tmp
        print(1)
