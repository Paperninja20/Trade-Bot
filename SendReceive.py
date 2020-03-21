from twilio.rest import Client
from flask import Flask, request, redirect
import Trade
import os
import robin_stocks as r
from twilio.twiml.messaging_response import MessagingResponse

account_sid = os.environ.get('Twilio_SID')
auth_token = os.environ.get('Auth_Token')

client = Client(account_sid, auth_token)

months = {          #Dictionary to help with searching and formatting
    'JAN': '01',
    'FEB': '02',
    'MAR': '03',
    'APR': '04',
    'MAY': '05',
    'JUN': '06',
    'JUL': '07',
    'AUG': '08',
    'SEP': '09',
    'SEPT':'09',
    'OCT': '10',
    'NOV': '11',
    'DEC': '12'
}

app = Flask(__name__)

@app.route("/")
def index():
    return "Pog"



@app.route("/receivesms", methods = ['GET', 'POST'])
def ReceiveSms():
    incomingMessage = request.values.get('Body')    #get body of text
    tokens = incomingMessage.split()                #split the text into a list of words
    del tokens[0:4]                                 #delete "Forwarded SMS of: STREAMALERTS"

    for word in tokens:
        if word[0] == '+':
            tokens.remove(word)

    if tokens[0] == 'New' and tokens[1][0] == 't':  #check if the stream alert is a play
        del tokens[0:5]                             #delete "New trade activity on stream:"
        if tokens[0] == 'SOLD':                     #check for sell
            exit()
        contract = parse(tokens)                    #search text for expiration date, strike price, and contract type
        ticker = 'NONE'                             #initialize ticker to NONE

        if contract[1][0] == '$':                           #check if Josh put both the month and the day or if it was just the month
            for x, y in zip(tokens[::], tokens[1::]):       #loop to find the ticker
                if x == contract[0]:
                    if y.isupper() and not any(ch.isdigit() for ch in y) and y != 'TRADE':
                        ticker = y
                if y == contract[0]:
                    if x.isupper() and not any(ch.isdigit() for ch in x) and x != 'TRADE':
                        ticker = x

            if ticker == 'NONE':                #if ticker was not found
                print('ticker not found!')
                exit()

            expirDate = getExpirDate(ticker, contract)      #correctly format the expiration date
            strike = contract[1]                            #set strike
            strikeIndex = 1                                 #remember the index of the strike
        else:
            for x, y in zip(tokens[::], tokens[1::]):       #loop to find the ticker
                if x == contract[1]:
                    if y.isupper() and not any(ch.isdigit() for ch in y) and y != 'TRADE':
                        ticker = y
                if y == contract[0]:
                    if x.isupper() and not any(ch.isdigit() for ch in x) and x != 'TRADE':
                        ticker = x

            if ticker == 'NONE':                #if ticker was not found
                print('ticker not found!')
                exit()

            expirDate = '2020-' + months[contract[0].upper()] + '-' + contract[1]       #correctly format the expiration date
            strike = contract[2]                                                        #set strike
            strikeIndex = 2                                                             #remember the index of the strike

        type = strike[-1].upper()       #store contract type

        if type == 'P':
            type = 'put'
            strike = strike[1:-1]       #remove the $ and the contract type
        elif type == 'C':
            type = 'call'
            strike = strike[1:-1]       #remove the $ and the contract type
        else:                           #if Josh put a space between the strike and the contract type
            strike = strike[1:]         #remove just the $
            if contract[strikeIndex + 1].upper() == 'C':
                type = 'call'
            elif contract[strikeIndex + 1].upper() == 'P':
                type = 'put'

        Trade.bank(ticker, expirDate, strike, type)     #call the main function with the parsed information

    return "pog"


#FUNCTION TO FIND THE EXPIRATION DATE, STRIKE PRICE, AND CONTRACT TYPE
def parse(wordList):
    optionInfo = []     #initialize list to store the expiration date, strike price, and contract type

    for word in wordList:                                       #check each word in the text
        if not any(ch.isdigit() for ch in word):                    #if the word has no numbers
            if word.upper() == 'P' or word.upper() == 'C':              #if the word indicates the contract type, save the word to the list
                optionInfo.append(word)
                continue
            if word.upper() not in months:                              #if the word is not the expiration month, ignore it
                continue
        if word[0] == '+' or word[0] == '.' or word == '2quit' or '/' in word:     #if the word has a number, check if it indicates how many contracts Josh got or what price he got it at, or if its 2quit. Ignore these if so
            continue
        optionInfo.append(word)                                     #if the word passes all the filters, add it to the list

    return optionInfo                                           #return the list



#FUNCTION TO FIND THE EXPIRATION DATE IF HE ONLY PUT THE MONTH AND NOT THE DAY
def getExpirDate(symbol, contract):
    month = '-' + months[contract[0].upper()] + '-'
    possibleExpirs = r.get_chains(symbol, info = 'expiration_dates')

    for date in possibleExpirs:
        if month in date:
            return date



if __name__ == "__main__":
    app.run(debug=True)
