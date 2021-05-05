#!python3

import time
import argparse
import scrapy.crawler
import twisted.internet
import scrapy.utils.log
import scrapy.utils.project

limit = True
max_size = 100
format = 'json'
spiders = ['countries', 'cities', 'prices']

parser = argparse.ArgumentParser(prog='run', description='Numbeo scraper CLI.')

parser.add_argument('-l', '--limit', action='store_true', dest='limit')
parser.add_argument('-n', '--no-limit', action='store_false', dest='limit')
parser.add_argument('-m', '--max-size', default=max_size, type=int)
parser.add_argument('-f', '--format', default=format, type=str)
parser.add_argument('-s', '--spiders', nargs='+', default=spiders, type=str)

parser.set_defaults(limit=limit)

args = parser.parse_args()

settings = scrapy.utils.project.get_project_settings()

pipeline = {
    'csv': 'numbeo.pipelines.CSVPipeline',
    'json': 'numbeo.pipelines.JSONPipeline',
    'xml': 'numbeo.pipelines.XMLPipeline',
}[args.format]

settings['ITEM_PIPELINES'] = {pipeline: 300}

settings['FEEDS'] = {spider: {'format': args.format} for spider in args.spiders}

scrapy.utils.log.configure_logging({'LOG_LEVEL': 'CRITICAL'})

runner = scrapy.crawler.CrawlerRunner(settings)


@twisted.internet.defer.inlineCallbacks
def crawl():
    durations = []
    for spider in args.spiders:
        print(f"Running spider '{spider}'...")
        start = time.time()
        yield runner.crawl(spider, limit=args.limit, max_size=args.max_size)
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
