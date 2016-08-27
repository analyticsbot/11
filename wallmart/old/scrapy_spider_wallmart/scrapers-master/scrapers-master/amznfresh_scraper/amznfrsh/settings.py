# -*- coding: utf-8 -*-

# Scrapy settings for amznfrsh project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'amznfrsh'

SPIDER_MODULES = ['amznfrsh.spiders']
NEWSPIDER_MODULE = 'amznfrsh.spiders'

DATABASE = {'drivername' : 'mysql+mysqlconnector',
			'host' : '104.131.84.120',
			'port' : '3306',
			'username' : 'dev',
			'password' : 'ilikerandompasswords',
			'database' : 'banana_now'
}

ITEM_PIPELINES = {
    'amznfrsh.pipelines.AmznfrshPipeline': 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'amznfrsh (+http://www.yourdomain.com)'
