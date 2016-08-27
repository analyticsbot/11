from sqlalchemy.orm import sessionmaker
from models import Product, db_connect, create_product_table

class WalmartScraperPipeline(object):
	def __init__(self):
		engine = db_connect()
		create_product_table(engine)
		self.Session = sessionmaker(bind=engine)

	def process_item(self, item, spider):
		session = self.Session()
		product = Product(**item)

		try:
			session.add(product)
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()

		return item
