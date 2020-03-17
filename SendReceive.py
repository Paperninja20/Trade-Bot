from twilio.rest import Client
from flask import Flask, request, redirect
import Trade
import robin_stocks as r
from twilio.twiml.messaging_response import MessagingResponse

account_sid = "AC8e9b970324d70067800ef0ca54ae85e0"
auth_token = "010b996fa537e0859cc07c512fbcd56c"

client = Client(account_sid, auth_token)

months = {
    "JAN": "01",
    "FEB": "02",
    "MAR": "03",
    "APR": "04",
    "MAY": "05",
    "JUN": "06",
    "JUL": "07",
    "AUG": "08",
    "SEP": "09",
    "OCT": "10",
    "NOV": "11",
    "DEC": "12"
}

app = Flask(__name__)

@app.route("/")
def index():
    return "lol"

@app.route("/receivesms", methods = ['GET', 'POST'])
def ReceiveSms():
    incomingMessage = request.values.get('Body')
    Jacob = "+14089921595"
    Corey = "+15103756729"

    '''client.messages.create(
        to = Jacob,
        from_= "+18163992829",
        body = incomingMessage
        )

    client.messages.create(
        to = Corey,
        from_= "+18163992829",
        body = incomingMessage
        )'''


    tokens = incomingMessage.split()
    del tokens[0:4]
    if tokens[0] == 'New' and tokens[1] == 'trade':
        del tokens[0:5]
        ticker = tokens[0]
        contract = parse(tokens)
        if contract[1][0] == '$':
            expirDate = getExpirDate(ticker, contract)
            strike = contract[1]
            strikeIndex = 1
        else:
            expirDate = '2020-' + months[contract[0].upper()] + '-' + contract[1]
            strike = contract[2]
            strikeIndex = 2
        print(expirDate)
        type = strike[-1].upper()
        if type == 'P':
            type = 'put'
            strike = strike[1:-1]
        elif type == 'C':
            type = 'call'
            strike = strike[1:-1]
        else:
            strike = strike[1:]
            if contract[strikeIndex + 1].upper() == 'C':
                type = 'call'
            elif contract[strikeIndex + 1].upper() == 'P':
                type = 'put'
        print(strike)
        print(type)

        Trade.bank(ticker, expirDate, strike, type)


    return "pog"

def parse(wordList):

    '''make this a dictionary with key as JAN/FEB/MAR and value as 01/02/03'''

    optionInfo = []

    for word in wordList:
        if not any(ch.isdigit() for ch in word):
            if word.upper() == 'P' or word.upper() == 'C':
                optionInfo.append(word)
                continue
            if word.upper() not in months:
                continue
        if word[0] == '+' or word[0] == '.' or word == '2quit':
            continue
        optionInfo.append(word)

    return optionInfo

def getExpirDate(symbol, contract):
    month = '-' + months[contract[0].upper()] + '-'
    possibleExpirs = r.options.get_chains(symbol, info = 'expiration_dates')
    for date in possibleExpirs:
        if month in date:
            return date

'''def SendSms(incomingMessage):
    Jacob = "+14089921595"
    Corey = "+15103756729"

    client.messages.create(
        to = Jacob,
        from_= "+18163992829",
        body = incomingMessage
        )

    client.messages.create(
        to = Corey,
        from_= "+18163992829",
        body = incomingMessage
        )'''

if __name__ == "__main__":
    app.run(debug=True)