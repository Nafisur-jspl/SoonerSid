# Handles all the post request received by the server
# Takes decision on what to do
# Has connection Establisher

import sys
from ConnectionEstablisher import ConnectionEstablisher
import json
import os
import requests


class ChatHandler(object):

    def __init__(self):
        self.connection = ConnectionEstablisher()

    # Reads the message, handles what to do with the message

    def decision_maker(self, requests, data):
        user_id, text = self.receive_message(data)
        apiai_response = self.call_apiai(text)
        self.send_message(user_id, apiai_response, requests)
        if self.connection.dbrecord_exists(user_id=user_id) is False:
            self.connection.dbrecord_insert(user_id=user_id)

    def call_apiai(self, text):
        response_json = self.connection.api_connect(text)
        return response_json['result']['fulfillment']['speech']

    def receive_message(self, data):
        log(data)
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):  # someone sent us a message

                        sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"]["text"]  # the message's text

                        return sender_id, message_text

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass

    def send_message(self, recipient_id, message_text, requests):

        self.log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            self.log(r.status_code)
            self.log(r.text)

    def log(message):  # simple wrapper for logging to stdout on
        sys.stdout.flush()
