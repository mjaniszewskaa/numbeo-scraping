import csv
import tqdm
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

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CitiesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=scrapy.signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        self.pbar = tqdm.tqdm(total=len(self.start_urls))
        with open('/home/bartek/numbeo-scraping/scrapy/log1.txt', 'wt') as f:
            f.write('Opened.\n')

    def spider_closed(self, spider):
        self.pbar.close()
        with open('/home/bartek/numbeo-scraping/scrapy/log2.txt', 'wt') as f:
            f.write('Closed.\n')

    def parse(self, response):
        self.pbar.update(1)
        country = response.xpath('//span[@itemprop="name"]/text()')[1]
        for s in response.xpath('//*[@id="city"]/option//@value')[1:]:
            yield numbeo.items.City(country.get(), s.get())
