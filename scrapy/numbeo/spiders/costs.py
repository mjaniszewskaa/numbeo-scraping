import csv
import scrapy
import numbeo.items

url = 'https://www.numbeo.com/cost-of-living/city_result.jsp?country={}&city={}&displayCurrency=USD'


class CostsSpider(scrapy.Spider):
    name = 'costs'

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
        for row in filter(lambda row: row.xpath('td'), selection):
            costs = numbeo.items.Costs()
            location = '//html/body/div[2]//span[@itemprop="name"]/text()'
            costs['Country'] = response.xpath(location)[1].get().strip()
            costs['City'] = response.xpath(location)[2].get().strip()
            costs['Name'] = row.xpath('td/text()').get().strip()
            costs['Mid'] = row.xpath('td/span/text()').get().strip('$').strip()
            for bound in ['Left', 'Right']:
                xpath = f'td/span[@class="barText{bound}"]/text()'
                try:
                    costs[bound] = row.xpath(xpath).get().strip()
                except:
                    costs[bound] = 'NaN'
            yield costs
