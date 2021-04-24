import scrapy
import numbeo.items


class CountriesSpider(scrapy.Spider):
    name = 'countries'

    def __init__(self, **kwargs):
        self.start_urls = ['https://www.numbeo.com/cost-of-living/']
        super().__init__(**kwargs)

    def parse(self, response):
        xpath = '//html/body/div[2]/div[6]/table//@href'
        selection = response.xpath(xpath)
        for s in selection:
            yield numbeo.items.Link(self.start_urls[0] + s.get())
