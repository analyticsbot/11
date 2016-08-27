# Scrapy settings for walmart_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'walmart_scraper'

SPIDER_MODULES = ['walmart_scraper.spiders']
NEWSPIDER_MODULE = 'walmart_scraper.spiders'

DATABASE = {'drivername' : 'mysql+mysqlconnector',
			'host' : '104.131.84.120',
			'port' : '3306',
			'username' : 'dev',
			'password' : 'ilikerandompasswords',
			'database' : 'banana_now'
}

ITEM_PIPELINES = {
    'walmart_scraper.pipelines.WalmartScraperPipeline': 300,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'walmart_scraper (+http://www.yourdomain.com)'
