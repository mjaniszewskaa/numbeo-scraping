import csv
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

    def parse(self, response):
        xpath = '//html/body/div[2]/table//tr'
        selection = response.xpath(xpath)
        loc = response.xpath('//span[@itemprop="name"]/text()')[1:]
        print(response.request.url)
        for row in filter(lambda row: row.xpath('td'), selection):
            prices = numbeo.items.Prices()
            prices['Country'], prices['City'] = [l.get().strip() for l in loc]
            prices['Name'] = row.xpath('td/text()').get().strip()
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
