BOT_NAME = 'numbeo'

SPIDER_MODULES = ['numbeo.spiders']
NEWSPIDER_MODULE = 'numbeo.spiders'

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1e-2

LOG_LEVEL = 'INFO'
LOG_FILE = 'scrapy.log'
