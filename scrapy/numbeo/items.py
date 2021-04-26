import scrapy


class Country(scrapy.Item):
    country = scrapy.Field()

    def __init__(self, country):
        super(Country, self).__init__()
        self['country'] = country


class City(scrapy.Item):
    country = scrapy.Field()
    city = scrapy.Field()

    def __init__(self, country, city):
        super(City, self).__init__()
        self['country'] = country
        self['city'] = city


class Costs(scrapy.Item):
    city = scrapy.Field()
    name = scrapy.Field()
    mid = scrapy.Field()
    left = scrapy.Field()
    right = scrapy.Field()
