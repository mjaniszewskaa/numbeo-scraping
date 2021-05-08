import scrapy
import scrapy.exporters


class Pipeline:

    format = None
    export_function = None

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.opened, scrapy.signals.spider_opened)
        crawler.signals.connect(pipeline.closed, scrapy.signals.spider_closed)
        return pipeline

    def opened(self, spider):
        file = open(f'{spider.name}.{self.format}', 'wb')
        exporter_name = f'{self.format.capitalize()}ItemExporter'
        self.files[spider] = file
        self.exporter = getattr(scrapy.exporters, exporter_name)(file)
        self.exporter.fields_to_export = {
            'countries': ['Country'],
            'cities': ['Country', 'City'],
            'prices': ['Country', 'City', 'Category', 'Name', 'Price', 'Min', 'Max'],
        }[spider.name]
        self.exporter.start_exporting()

    def closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class CSVPipeline(Pipeline):

    format = 'csv'


class JSONPipeline(Pipeline):

    format = 'json'


class XMLPipeline(Pipeline):

    format = 'xml'
