#from sqlalchemy.orm import sessionmaker
#from models import Restaurants, db_connect, create_table

class EaterPipeline(object):
    #def __init__(self):
        #engine = db_connect()
        #create_table(engine)
        #self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        return item
        #session = self.Session()
        #restaurant = Restaurants(**item) 

        #try:
            #session.add(restaurant)
            #session.commit()
        #except:
            #session.rollback()
            #raise
        #finally:
            #session.close()

        #return item
