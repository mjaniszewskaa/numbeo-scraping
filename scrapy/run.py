#!python3

import os
import time
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
    durations = []
    for spider in ['countries', 'cities', 'prices']:
        with contextlib.suppress(FileNotFoundError):
            os.remove(f'{spider}.{format}')
        settings['FEEDS'] = {f'{spider}.{format}': {'format': format}}
        settings['FEED_EXPORT_FIELDS'] = {
            'countries': ['Country'],
            'cities': ['Country', 'City'],
            'prices': ['Country', 'City', 'Category', 'Name', 'Price', 'Min', 'Max'],
        }[spider]
        print(f"Running spider '{spider}'...")
        start = time.time()
        yield runner.crawl(spider, limit=limit, max_size=max_size)
        end = time.time()
        duration = round(end - start, 2)
        print(f'Spider {spider} took {duration}s.')
        durations.append(duration)
    total_duration = round(sum(durations), 2)
    print(f'Total elapsed time: {total_duration}s.')
    twisted.internet.reactor.stop()


if __name__ == '__main__':
    crawl()
    twisted.internet.reactor.run()
