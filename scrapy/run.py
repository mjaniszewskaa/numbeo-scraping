#!python3

import time
import argparse
import scrapy.crawler
import twisted.internet
import scrapy.utils.log
import scrapy.utils.project

__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))

limit = True
max_size = 100
format = 'csv'
spiders = ['countries', 'cities', 'prices']

parser = argparse.ArgumentParser(prog='run', description='Numbeo scraper CLI.')

parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument('-l', '--limit', action='store_true', dest='limit')
parser.add_argument('-n', '--no-limit', action='store_false', dest='limit')
parser.add_argument('-m', '--max-size', default=max_size, type=int)
parser.add_argument('-f', '--format', default=format, type=str)
parser.add_argument('-s', '--spiders', default=3, type=int)

parser.set_defaults(limit=limit)

args = parser.parse_args()

settings = scrapy.utils.project.get_project_settings()

pipeline_name = f'numbeo.pipelines.{args.format.upper()}Pipeline'
settings['ITEM_PIPELINES'] = {pipeline_name: 300}

scrapy.utils.log.configure_logging({'LOG_LEVEL': 'CRITICAL'})

runner = scrapy.crawler.CrawlerRunner(settings)


@twisted.internet.defer.inlineCallbacks
def crawl():
    durations = []
    params = {'limit': args.limit, 'max_size': args.max_size}
    for i, spider in enumerate(spiders[:args.spiders]):
        params['input'] = f'{spiders[i - 1]}.{args.format}'
        print(f"Running spider '{spider}'...")
        start = time.time()
        yield runner.crawl(spider, **params)
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
