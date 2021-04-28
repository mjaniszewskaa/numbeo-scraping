import scrapy


class Country(scrapy.Item):
    Country = scrapy.Field()

    def __init__(self, country):
        super(Country, self).__init__()
        self['Country'] = country


class City(scrapy.Item):
    Country = scrapy.Field()
    City = scrapy.Field()

    def __init__(self, country, city):
        super(City, self).__init__()
        self['Country'] = country
        self['City'] = city


class Prices(scrapy.Item):
    Country = scrapy.Field()
    City = scrapy.Field()
    Category = scrapy.Field()
    Name = scrapy.Field()
    Price = scrapy.Field()
    Min = scrapy.Field()
    Max = scrapy.Field()
