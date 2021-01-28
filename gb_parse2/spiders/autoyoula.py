import scrapy
from ..loaders import AutoyoulaLoader


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    css_query = {
        'brands': 'div.TransportMainFilters_block__3etab a.blackLink',
        'pagination': 'div.Paginator_block__2XAPy a.Paginator_button__u1e7D',
        'ads': 'article.SerpSnippet_snippet__3O1t2 a.blackLink',
    }

    xpath_query = {
        'brands': "//div[@class='TransportMainFilters_brandsList__2tIkv']//a[@data-target='brand']/@href",
        'pagination': "//div[contains(@class, 'Paginator_block')]/a[contains(@class, 'Paginator_button')]/href",
        'ads': "//artical[contains(@data-target, 'serp-snippet')]/a[contains(data-target, 'serp-snippet-title')]/@href",
    }

    data_query = {
        'title': 'div.AdvertCard_advertTitle__1S1Ak::text',
        'price': 'div.AdvertCard_price__3dDCr::text',

    }

    itm_tamplate = {
        'title': '//div[@data-target="advert-title"]/text()',
        'images': '//figure[contains(@class, "PhotoGallery_photo")]//img/@scr',
        'descripton': '//div[contains(@class, "AdvertCard_descriptionInner")]/text()',
        'author': '//script[contains(text(), "window.transitState =")]/text()',
        'specifications': '//div[contains(@class, "AdvertCard_specs")]/div/div[contains(@class, "AdvertSpecs_row")]',
        'price': '//div[contains(@class, "AdvertCard_priceBlock")]/div[data-target="advert-price"]/text()',
    }

    def parse(self, response, **kwargs):
        brands_links = response.xpath(self.xpath_query['brands'])
        yield from self.gen_task(response, brands_links, self.brand_parse)

    def brand_parse(self, response):
        pagination_links = response.xpath(self.xpath_query['pagination'])
        yield from self.gen_task(response, pagination_links, self.brand_parse)
        ads_links = response.xpath(self.xpath_query['ads'])
        yield from self.gen_task(response, ads_links, self.ads_parse)

    def ads_parse(self, response):
        loader = AutoyoulaLoader(response=response)
        loader.add_value('url', response.url)
        for key, selector in self.itm_tamplate.items():
            loader.add_xpath(key, selector)
        item = loader.load_item()
        yield item

    @staticmethod
    def gen_task(response, link_list, callback):
        for link in link_list:
            yield response.follow(link, callback=callback)