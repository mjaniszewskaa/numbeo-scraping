import re
import scrapy
import numbeo.items


class CostsSpider(scrapy.Spider):
    name = 'costs'

    def __init__(self, input, limit=False, max_size=100, **kwargs):
        try:
            with open(input, "rt") as f:
                self.start_urls = [url.strip() for url in f.readlines()[1:]]
        except:
            self.start_urls = []
        if limit:
            self.start_urls = self.start_urls[:2*max_size]
        super().__init__(**kwargs)

    def parse(self, response):
        xpath = '//html/body/div[2]/table//tr'
        selection = response.xpath(xpath)
        for row in selection:
            costs = numbeo.items.Costs()
            if row.xpath('td'):
                url = response.request.url
                costs['city'] = re.findall('/in/(.*)', url)[0].strip()
                costs['name'] = row.xpath('td/text()').get().strip()
                costs['mid'] = row.xpath(
                    'td/span/text()').get().replace('$', '').strip()
                try:
                    costs['left'] = row.xpath(
                        'td/span[@class="barTextLeft"]/text()').get().strip()
                except:
                    costs['left'] = 'NaN'
                try:
                    costs['right'] = row.xpath(
                        'td/span[@class="barTextRight"]/text()').get().strip()
                except:
                    costs['right'] = 'NaN'
                yield costs
