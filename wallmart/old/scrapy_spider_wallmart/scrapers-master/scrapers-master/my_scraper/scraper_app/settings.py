BOT_NAME = 'livingsocial'

SPIDER_MODULES = ['scraper_app.spiders']

DATABASE = {'drivername' : 'mysql',
			'host' : 'localhost',
			'port' : '3306',
			'username' : 'root',
			'password' : 'root',
			'database' : 'banana_now'}

ITEM_PIPELINES = ['scraper_app.pipelines.LivingSocialPipeline']