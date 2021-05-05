import tqdm
import pandas
import scrapy
import numbeo.items

url = 'https://www.numbeo.com/cost-of-living/country_result.jsp?country={}'


class CitiesSpider(scrapy.Spider):
    name = 'cities'

    def __init__(self, limit=True, max_size=100, **kwargs):
        self.limit = limit
        self.max_size = max_size
        super().__init__(**kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CitiesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.opened, scrapy.signals.spider_opened)
        crawler.signals.connect(spider.closed, scrapy.signals.spider_closed)
        return spider

    def opened(self, spider):
        format = self.settings['FEEDS'][self.name]['format']
        try:
            reader = getattr(pandas, f'read_{format}')
            entries = reader(f'countries.{format}')[['Country']].values
            self.start_urls = [url.format(*entry) for entry in entries]
        except:
            self.start_urls = []
        if self.limit:
            self.start_urls = self.start_urls[:self.max_size]
        self.progressbar = tqdm.tqdm(total=len(self.start_urls))

    def closed(self, spider):
        self.progressbar.close()

    def parse(self, response):
        self.progressbar.update(1)
        country = response.xpath('//span[@itemprop="name"]/text()')[1]
        for s in response.xpath('//*[@id="city"]/option//@value')[1:]:
            yield numbeo.items.City(country.get(), s.get())
