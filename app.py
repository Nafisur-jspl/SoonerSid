import os
import requests
from flask import Flask, request
from ChatHandler import ChatHandler

app = Flask(__name__)
chatter = ChatHandler()


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
def web_hook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    chatter.decision_maker(data, requests)

    return "ok", 200

if __name__ == '__main__':
    app.run(debug=True)
