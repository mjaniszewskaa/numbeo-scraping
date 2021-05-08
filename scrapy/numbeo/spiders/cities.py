import tqdm
import pandas
import scrapy
import numbeo.items

url = 'https://www.numbeo.com/cost-of-living/country_result.jsp?country={}'


class CitiesSpider(scrapy.Spider):
    name = 'cities'

    def __init__(self, input, limit=True, max_size=100, **kwargs):
        self.input = input
        self.limit = limit
        self.max_size = max_size
        format = input.split('.')[-1]
        reader = getattr(pandas, f'read_{format}')
        entries = reader(input)[['Country']].values
        self.start_urls = [url.format(*entry) for entry in entries]
        if limit:
            self.start_urls = self.start_urls[:max_size]
        super().__init__(**kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spdr = super(CitiesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spdr.opened, scrapy.signals.spider_opened)
        crawler.signals.connect(spdr.closed, scrapy.signals.spider_closed)
        return spdr

    def opened(self, spider):
        self.progressbar = tqdm.tqdm(total=len(self.start_urls))

    def closed(self, spider):
        self.progressbar.close()

    def parse(self, response):
        self.progressbar.update(1)
        country = response.xpath('//span[@itemprop="name"]/text()')[1]
        for s in response.xpath('//*[@id="city"]/option//@value')[1:]:
            yield numbeo.items.City(country.get(), s.get())
