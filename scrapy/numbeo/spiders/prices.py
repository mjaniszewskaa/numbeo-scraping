import tqdm
import pandas
import scrapy
import numbeo.items

url = 'https://www.numbeo.com/cost-of-living/city_result.jsp?country={}&city={}&displayCurrency=USD'


class PricesSpider(scrapy.Spider):
    name = 'prices'

    def __init__(self, input, limit=True, max_size=100, **kwargs):
        self.input = input
        self.limit = limit
        self.max_size = max_size
        format = input.split('.')[-1]
        reader = getattr(pandas, f'read_{format}')
        entries = reader(input)[['Country', 'City']].values
        self.start_urls = [url.format(*entry) for entry in entries]
        if self.limit:
            self.start_urls = self.start_urls[:max_size]
        super().__init__(**kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spdr = super(PricesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spdr.opened, scrapy.signals.spider_opened)
        crawler.signals.connect(spdr.closed, scrapy.signals.spider_closed)
        return spdr

    def opened(self, spider):
        self.progressbar = tqdm.tqdm(total=len(self.start_urls))

    def closed(self, spider):
        self.progressbar.close()

    def parse(self, response):
        self.progressbar.update(1)
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
