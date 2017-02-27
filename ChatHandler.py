# Handles all the post request received by the server
# Takes decision on what to do
# Has connection Establisher

from ConnectionEstablisher import ConnectionEstablisher


class ChatHandler(object):

    def __init__(self):
        self.connection = ConnectionEstablisher()

    # Reads the message, handles what to do with the message
    # Responds back what to send back

    def decision_maker(self, text, user_id):
        apiai_response = self.call_apiai(text)
        if self.connection.dbrecord_exists(user_id=user_id) is False:
            self.connection.dbrecord_insert(user_id=user_id)
        return apiai_response

    def call_apiai(self, text):
        response_json = self.connection.api_connect(text)
        return response_json['result']['fulfillment']['speech']


