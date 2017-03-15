import os
import sys
import json
import requests
from flask import Flask, request
from ConnectionEstablisher import ConnectionEstablisher
from ChatHandler import ChatHandler
import ast

app = Flask(__name__)
connection = ConnectionEstablisher()
chatter = ChatHandler()

userInfo = False

designation = { "undergraduate": "DEVELOPER_DEFINED_PAYLOAD_FOR_UNDERGRADUATE",
              "graduate": "DEVELOPER_DEFINED_PAYLOAD_FOR_GRADUATE",
              "PHD": "DEVELOPER_DEFINED_PAYLOAD_FOR_PHD",
              "Professor": "DEVELOPER_DEFINED_PAYLOAD_FOR_PROFESSOR"
              }

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    # Sending the message to API.AI , db checks are done and the decision maker
                    # returns back the appropriate return

                    if userInfo and message_text in designation.keys():
                        connection.dbrecord_update(user_id=sender_id, designation=message_text)
                    else:
                        send_message(sender_id, "got it, thanks!")  # To make sure the application is running
                        send_message(sender_id, textReply(message_text))
                    if not connection.dbrecord_exists(user_id=sender_id):
                        getUserInfo(sender_id)

                    # quick_replies(sender_id, "Pick a color") # Checking quick replies

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def getUserInfo(sender_id):
    connection.dbrecord_insert(user_id=sender_id)
    quick_replies(sender_id, designation, option_header='Select Your Designation')
    userInfo = True


def textReply(text):
    response_json = connection.api_connect(text)
    return response_json['result']['fulfillment']['speech']


def send_message(recipient_id, message_text):
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
        log(r.status_code)
        log(r.text)

# composes data for a quick reply. Gets the options and the payload as dictionary
# along with option header and recipient ID

def getquickContent(dummy, option_header, sender_id):
    quickContent = []
    for key, value in dummy.items():
        quickContent.append('{"content_type": "text", "title":"' + key +'", "payload":"' + value + '"}')
    return '{ "recipient": { "id" :' + sender_id + '},' + '"message": { "text": "'+ option_header +'", "quick_replies": [' + (','.join(quickContent)) + ']}}'

def quick_replies(recipient_id, designation, option_header):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps(ast.literal_eval(getquickContent(designation, option_header, recipient_id)))
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)

