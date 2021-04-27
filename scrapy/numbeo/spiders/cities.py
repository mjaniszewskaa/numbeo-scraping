import csv
import scrapy
import numbeo.items

url = 'https://www.numbeo.com/cost-of-living/country_result.jsp?country={}'


class CitiesSpider(scrapy.Spider):
    name = 'cities'

    def __init__(self, limit=True, max_size=100, **kwargs):
        try:
            with open('countries.csv', 'rt') as f:
                entries = list(csv.reader(f))[1:]
            self.start_urls = [url.format(*entry) for entry in entries]
        except:
            self.start_urls = []
        if limit:
            self.start_urls = self.start_urls[:max_size]
        super().__init__(**kwargs)

    def parse(self, response):
        xpath = '//*[@id="city"]/option//@value'
        selection = response.xpath(xpath)
        country = response.xpath('//span[@itemprop="name"]/text()')[1]
        for s in selection[1:]:
            yield numbeo.items.City(country.get(), s.get())
