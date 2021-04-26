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


class Costs(scrapy.Item):
    Country = scrapy.Field()
    City = scrapy.Field()
    Name = scrapy.Field()
    Mid = scrapy.Field()
    Left = scrapy.Field()
    Right = scrapy.Field()
