import re
import scrapy
import numbeo.items


def sanitize(input):
    return re.sub('[(),]', '', re.sub('[ +]', '-', input))


class CitiesSpider(scrapy.Spider):
    name = 'cities'

    def __init__(self, input, limit=False, max_size=100, **kwargs):
        try:
            with open(input, "rt") as f:
                self.start_urls = [url.strip() for url in f.readlines()[1:]]
        except:
            self.start_urls = []
        if limit:
            self.start_urls = self.start_urls[:max_size]
        super().__init__(**kwargs)

    def parse(self, response):
        xpath = '//*[@id="city"]/option//@value'
        selection = response.xpath(xpath)
        country = response.request.url[response.request.url.find('=') + 1:]
        for s in selection:
            city = "https://www.numbeo.com/cost-of-living/in/" + s.get()
            yield numbeo.items.Link(sanitize(city))
            yield numbeo.items.Link(sanitize(f'{city}-{country}'))
