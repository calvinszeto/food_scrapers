# Scrapy settings for category project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'category'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['category.spiders']
NEWSPIDER_MODULE = 'category.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

DOWNLOAD_DELAY = 2.5
LOG_FILE="category.log"
