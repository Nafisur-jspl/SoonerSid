# A Class that can establish a connection with ApiConnector
# and MongoConnector and fetches the existing environment variables
# and sets them up for connection

import json
import os
import uuid

from ApiConnector import ApiConnector
from MongoConnector import MongoConnector


class ConnectionEstablisher(object):

    # Defining the local environment variables
    # Needed for API.AI and Mongo Client

    MONGODB_ACCESS = "DB_ACCESS"
    APICLIENT_ACCESS_TOKEN = "CLIENT_ACCESS_TOKEN"
    LANGUAGE = "en"
    DB_NAME = 'heroku_swknz2mg'
    TABLE_NAME = 'userinfo'

    def __init__(self):
        self.session = self.create_sessionid()
        self.apicat = self.get_envariable(ConnectionEstablisher.APICLIENT_ACCESS_TOKEN)
        self.mongoaccess = self.get_envariable(ConnectionEstablisher.MONGODB_ACCESS)
        self.apisecure = ApiConnector(self.session, self.LANGUAGE, self.apicat)
        self.mongoclient = MongoConnector(self.mongoaccess)

    # A function for creating a unique session id when establishing
    # a connection with API.ai server, 36 is the limit for a api.ai server
    def create_sessionid(self):
        return str(uuid.uuid4())[:36]

    # Gets the environment variable from the local OS
    def get_envariable(self, vname):
        return os.getenv(vname)

    # Connects to the API.AI by sending in the text
    # Gets back the http response object and converts them into json and
    # returns it back
    def api_connect(self, text):
        self.apisecure = ApiConnector(session_id=self.session, lang=self.LANGUAGE, cat=self.apicat) # cat - Client Access Token
        response = self.apisecure.send_textquery(text).read()
        response_json = json.loads(response.decode('utf-8'))
        return response_json

    # db functions like checking for a record, insert, delete that calls MongoConnectors functions

    def dbrecord_exists(self, **fields):
        if self.mongoclient.record_exists(DB=ConnectionEstablisher.DB_NAME, TABLE=ConnectionEstablisher.TABLE_NAME, **fields):
            return True
        else:
            return False

    def dbrecord_insert(self, **fields):
            self.mongoclient.insert(ConnectionEstablisher.DB_NAME, ConnectionEstablisher.TABLE_NAME, **fields)

    def dbrecord_update(self, user_id, **fields):
            self.mongoclient.update(DB=ConnectionEstablisher.DB_NAME, TABLE=ConnectionEstablisher.TABLE_NAME, user_id=user_id, **fields)







