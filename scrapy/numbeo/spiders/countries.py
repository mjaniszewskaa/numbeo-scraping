import scrapy
import numbeo.items


class CountriesSpider(scrapy.Spider):
    name = 'countries'

    def __init__(self, **kwargs):
        self.start_urls = ['https://www.numbeo.com/cost-of-living/']
        super().__init__(**kwargs)

    def parse(self, response):
        for s in response.xpath('//html/body/div[2]/div[6]/table//a/text()'):
            yield numbeo.items.Country(s.get())
