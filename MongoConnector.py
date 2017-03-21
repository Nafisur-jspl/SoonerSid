# Mongo Connector that manages the connection made between the server
# and the MLAB mongo service
#Sooner
from pymongo import MongoClient

from UserDefinedExceptions.ElementAlreadyExists import ElementAlreadyExists
from UserDefinedExceptions.ElementDoesntExist import ElementDoesntExist

DB_NAME = 'heroku_swknz2mg'
TABLE_NAME = 'userinfo'


class MongoConnector(object):

    def __init__(self, db_access):
        self.db_client = MongoClient(db_access)

    # kwargs is of the type dict thus makes it easy to perform db operations which requires dict Data structure
    def record_exists(self, DB, TABLE, **fields):

        # How to combine strings to make a function call ?.
        # Workaround 1 getattributes cant pass an argument, Workaround 2 eval and exec are evil
        # Workaround 3 Hard code for now
        # db = "self.db_client"+"."+DB+"."+TABLE+"."
        # function_call = getattr(collection.Collection, 'find_one',kwargs)()

        if (self.db_client.heroku_swknz2mg.userinfo.find_one(fields)) is None:
            print("Element doesnt exists")
            return False
        else:
            print("Element Exists")
            return True

    def insert(self, DB, TABLE, **fields):
        try:
            if self.record_exists(DB=DB, TABLE=TABLE, **fields):
                raise ElementAlreadyExists("Element already exists")
            else:
                self.db_client.heroku_swknz2mg.userinfo.insert_one(fields)
                print("Element inserted")
        except ElementAlreadyExists as err:
                print(err)

    # Update is sufficient and findAndModify not considered because of a single thread access
    def update(self, DB, TABLE, user_id, **fields):
        if self.record_exists(DB=DB, TABLE=TABLE, **fields) is None:
            raise ElementDoesntExist("Element not present in the db")
        else:
            self.db_client.heroku_swknz2mg.userinfo.update_one({"user_id": user_id}, {"$set": fields})
            print ("Element Updated")














