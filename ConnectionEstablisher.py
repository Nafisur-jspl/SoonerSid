# A Class that can establish a connection with ApiConnector
# and MongoConnector and fetches the existing environment variables
# and sets them yp for connection

import os
import uuid
import json
from ApiConnector import ApiConnector


class ConnectionEstablisher(object):

    # Defining the local environment variables

    MONGODB_ACCESS = "DB_ACCESS"
    APICLIENT_ACCESS_TOKEN = "CLIENT_ACCESS_TOKEN"
    LANGUAGE = "en"

    def __init__(self):
        self.session = self.create_sessionid()
        self.apicat = self.get_envariable(ConnectionEstablisher.APICLIENT_ACCESS_TOKEN)
        self.mongoaccess = self.get_envariable(ConnectionEstablisher.MONGODB_ACCESS)
        self.apisecure = ApiConnector(self.session, self.LANGUAGE, self.apicat)

    # A function for creating a unique session id when establishing
    # a connection with API.ai server
    def create_sessionid(self):
        return str(uuid.uuid4())[:36]


    # Gets the anvironment variable from the local OS
    def get_envariable(self, vname):
        return os.getenv(vname)

    # Connects to the API.AI by sending in the text
    # Gets back the http response object and converts them into json and
    # returns it back
    def api_connect(self, text):
        self.apisecure = ApiConnector(self.session, self.LANGUAGE, self.apicat)
        response = self.apisecure.send_textquery(text).read()
        response_json = json.loads(response.decode('utf-8'))
        return response_json


