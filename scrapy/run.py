#!python3

import os
import contextlib
import scrapy.crawler
import twisted.internet
import scrapy.utils.project

limit = True
max_size = 100

format = 'csv'

settings = scrapy.utils.project.get_project_settings()

runner = scrapy.crawler.CrawlerRunner(settings)


@twisted.internet.defer.inlineCallbacks
def crawl():
    for spider in ['countries', 'cities', 'costs']:
        with contextlib.suppress(FileNotFoundError):
            os.remove(f'{spider}.{format}')
        settings['FEEDS'] = {f'{spider}.{format}': {'format': format}}
        settings['FEED_EXPORT_FIELDS'] = {
            'countries': ['country'],
            'cities': ['country', 'city'],
            'costs': ['city', 'name', 'mid', 'left', 'right'],
        }[spider]
        yield runner.crawl(spider, limit=limit, max_size=max_size)
    twisted.internet.reactor.stop()


if __name__ == '__main__':
    crawl()
    twisted.internet.reactor.run()
