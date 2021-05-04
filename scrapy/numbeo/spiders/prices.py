import csv
import tqdm
import scrapy
import numbeo.items

url = 'https://www.numbeo.com/cost-of-living/city_result.jsp?country={}&city={}&displayCurrency=USD'


class PricesSpider(scrapy.Spider):
    name = 'prices'

    def __init__(self, limit=True, max_size=100, **kwargs):
        try:
            with open('cities.csv', 'rt') as f:
                entries = list(csv.reader(f))[1:]
            self.start_urls = [url.format(*entry) for entry in entries]
        except:
            self.start_urls = []
        if limit:
            self.start_urls = self.start_urls[:max_size]
        super().__init__(**kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PricesSpider, cls).from_crawler(crawler, *args, **kwargs)
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
        loc_xpath = '//span[@itemprop="name"]/text()'
        location = [l.get().strip() for l in response.xpath(loc_xpath)[1:]]
        for row in response.xpath('//html/body/div[2]/table//tr'):
            if row.xpath('td'):
                prices = numbeo.items.Prices()
                prices['Country'], prices['City'] = location
                prices['Name'] = row.xpath('td/text()').get().strip()
                prices['Category'] = category
                try:
                    xpath = 'td/span/text()'
                    prices['Price'] = row.xpath(xpath).get().strip('$').strip()
                except:
                    prices['Price'] = 'NaN'
                for name, bound in zip(['Min', 'Max'], ['Left', 'Right']):
                    xpath = f'td/span[@class="barText{bound}"]/text()'
                    try:
                        prices[name] = row.xpath(xpath).get().strip()
                    except:
                        prices[name] = 'NaN'
                yield prices
            else:
                category = row.xpath('th/div/text()').get().strip()
