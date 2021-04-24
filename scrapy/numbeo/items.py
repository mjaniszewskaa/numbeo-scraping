import scrapy


class Link(scrapy.Item):
    link = scrapy.Field()

    def __init__(self, link):
        super(Link, self).__init__()
        self["link"] = link


class Costs(scrapy.Item):
    city = scrapy.Field()
    name = scrapy.Field()
    mid = scrapy.Field()
    left = scrapy.Field()
    right = scrapy.Field()
