from twilio.rest import Client
from flask import Flask, request, redirect

import receive
import robin_stocks as r

import os
from dotenv import load_dotenv

def main():
	load_dotenv()
	account_sid = os.getenv("ACCOUNT_SID")
	auth_token = os.getenv("AUTH_TOKEN")
	username = os.getenv("R_USER")
	password = os.getenv("R_PASSWORD")

	r.login(username = username, password = password)   #login here
	Client(account_sid, auth_token)

	app.run(debug=True)

app = Flask(__name__)

@app.route("/")
def index():
    return "PogBot now running."

@app.route("/receivesms", methods = ['GET', 'POST'])
def ReceiveSms():
    incomingMessage = request.values.get('Body') #get body of text
    res = receive.receive_msg(incomingMessage)
    if res == 0:
    	print("Not a new trade")
    elif res == 1:
    	print("Trade was a sell/close")
    elif res == 2:
    	print("Could not get ticker/strike")
    else:
    	print("Trade succeeded!")

    return "PogBot received the trade"

if __name__ == "__main__":
	main()
	
