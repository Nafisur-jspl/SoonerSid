# API Connector that manages the connection made between the server
# and the API.ai service

import apiai


class ApiConnector(object):

    def __init__(self, session_id, lang, cat):  # cat - Client Access Token
        self.session_id = session_id
        self.lang = lang
        self.cat = cat

    def get_lang(self):
        return self.lang

    def get_sessionid(self):
        return self.session_id

    def set_lang(self, lang):
        self.lang = lang

    # Makes an get api request and returns the http response object
    def send_textquery(self, text):
        ai_connection = apiai.ApiAI(self.cat)
        ai_request = ai_connection.text_request()
        ai_request.lang = self.lang
        ai_request.session_id = self.session_id
        ai_request.query = text
        ai_response = ai_request.getresponse()
        return ai_response
