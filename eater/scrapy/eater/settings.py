# Scrapy settings for eater project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'eater'

SPIDER_MODULES = ['eater.spiders']
NEWSPIDER_MODULE = 'eater.spiders'

ITEM_PIPELINES = ['eater.pipelines.EaterPipeline']

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'postgres',
            'password': 'okokok',
            'database': 'eater'}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'eater (+http://www.yourdomain.com)'
