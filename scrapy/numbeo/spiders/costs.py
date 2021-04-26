import re
import csv
import scrapy
import numbeo.items

url = 'https://www.numbeo.com/cost-of-living/city_result.jsp?country={}&city={}'


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
        for row in selection:
            costs = numbeo.items.Costs()
            if row.xpath('td'):
                costs['city'] = response.request.url.split("/")[-1]
                costs['name'] = row.xpath('td/text()').get().strip()
                costs['mid'] = row.xpath(
                    'td/span/text()').get().replace('$', '').strip()
                directions = ['left', 'right']
                for d in directions:
                    xpath = f'td/span[@class="barText{d.capitalize()}"]/text()'
                    try:
                        costs[d] = row.xpath(xpath).get().strip()
                    except:
                        costs[d] = 'NaN'
                yield costs
