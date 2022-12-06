# Make some requests to OpenAI's chatbot
import time
import os
import flask
import json
import re

# From https://github.com/rawandahmad698/PyChatGPT - Thanks!
from Classes import auth as Auth
from Classes import chat as Chat

from flask import g

global previous_convo_id
global access_token
APP = flask.Flask(__name__)

@APP.before_request
def before_request():
    g.previous_convo_id = None
    g.access_token = None

@APP.route("/chat", methods=["GET"])
def chat():
    message = flask.request.args.get("q")
    print("Sending message: ", message)
    g.access_token = Auth.get_access_token()

    if g.access_token == "":
        print("Access token is missing in /Classes/auth.json.")
        exit(1)

    answer, previous_convo = Chat.ask(auth_token=g.access_token,
                                      prompt=message,
                                      previous_convo_id=g.previous_convo_id)
    if answer == "400" or answer == "401":
        print("Your token is invalid. Attempting to refresh..")
        open_ai_auth = Auth.OpenAIAuth(email_address=email, password=password)
        open_ai_auth.begin()
        time.sleep(3)
        g.access_token = Auth.get_access_token()
    else:
        if previous_convo is not None:
            g.previous_convo_id = previous_convo
    
    print("Response: ", answer)
    return answer

def start_app():
    # Check if config.json exists
    if not os.path.exists("config.json"):
        print(">> config.json is missing. Please create it.")
        print("Exiting...")
        exit(1)

    # Read config.json
    with open("config.json", "r") as f:
        config = json.load(f)
        # Check if email & password are in config.json
        if "email" not in config or "password" not in config:
            print(">> config.json is missing email or password. Please add them.")
            print("Exiting...")
            exit(1)

    # Get email & password
    email = config["email"]
    password = config["password"]
    expired_creds = Auth.expired_creds()
    print("Checking if credentials are expired...")
    if expired_creds:
        print("Your credentials are expired." + " Attempting to refresh them...")
        open_ai_auth = Auth.OpenAIAuth(email_address=email, password=password)

        print("Credentials have been refreshed.")
        open_ai_auth.begin()
        time.sleep(3)
        is_still_expired = Auth.expired_creds()
        if is_still_expired:
            print("Failed to refresh credentials. Please try again.")
            exit(1)
        else:
            print("Successfully refreshed credentials.")
    else:
        print("Your credentials are valid.")

    print("Starting chat...")

    APP.run(port=31337, threaded=False)

if __name__ == "__main__":
    start_app()