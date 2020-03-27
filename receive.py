import trade
import robin_stocks as r
from datetime import datetime

def receive_msg(incomingMessage: str):
    """
    BOUGHT TO HEDGE OLD AAPL SHORT +20 May 15 AAPL $355C @ .80 NOT A RECOMENDATION DO NOT TRADE
    Rply STOP 2quit or HELP
    """
    tokens = incomingMessage.upper().split()        #split the text into a list of words
    del tokens[0:4]                                 #delete "Forwarded SMS of: STREAMALERTS"

    for word in tokens:
        if word[0] == '+':
            tokens.remove(word)

    if tokens[0] == 'NEW' and tokens[1][0] == 'T':  #check if the stream alert is a play
        del tokens[0:5]                             #delete "New trade activity on stream:"
        if tokens[0] in ['SOLD', 'CLOSED']:         #check for sell/closed
            return 1

        contract = getContractInfo(tokens)          #expiration date, strike price, and contract type
        result = getTickerAndStrike(contract, tokens)
        if not result:
            return 2

        ticker = result[0]
        strike = float(result[1])
        if strike > 150:
            return 3
        expirDate = result[2]
        optionType = result[3]

        trade.bank(ticker, expirDate, strike, optionType)     #call the main function with the parsed information
        return 4
    else:                                           #does not begin with "New T..."
        return 0


def getContractInfo(wordList: list):
    """
    FIND THE EXPIRATION DATE, STRIKE PRICE, AND CONTRACT TYPE
    """
    contractInfo = []                     #store the expiration date, strike price, and contract type
    for word in wordList:
        if not any(ch.isdigit() for ch in word):                    #if the word has no numbers
            if word in ['P', 'C']:          #if the word indicates the contract type, save the word to the list
                contractInfo.append(word)
                continue
            if word not in months:          #if the word is not the expiration month, ignore it
                continue
        if word[0] in ['+', '.'] or word == '2quit':  #if the word has a number, check if it indicates how many contracts Josh got or what price he got it at, or if its 2quit. Ignore these if so
            continue
        contractInfo.append(word)                     #if the word passes all the filters, add it to the list
    return contractInfo

def getTickerAndStrike(contract: list, tokens: list):
    ticker = False                                      #initialize ticker to None
    if contract[1][0] == '$':                           #May $355C
        for x, y in zip(tokens[::], tokens[1::]):       #loop to find the ticker
            if x == contract[0]:
                if not any(ch.isdigit() for ch in y) and y != 'TRADE':
                    ticker = y
            if y == contract[0]:
                if not any(ch.isdigit() for ch in x) and x != 'TRADE':
                    ticker = x

        if not ticker:                                      #if ticker was not found
            return False

        expirDate = getExpirDate(ticker, contract)      #correctly format the expiration date
        strike = contract[1]                            #set strike
        strikeIndex = 1
                                         #remember the index of the strike
    else:
        for x, y in zip(tokens[::], tokens[1::]):       #loop to find the ticker
            if x == contract[1]:
                if not any(ch.isdigit() for ch in y) and y != 'TRADE':
                    ticker = y
            if y == contract[0]:
                if not any(ch.isdigit() for ch in x) and x != 'TRADE':
                    ticker = x

        if not ticker:            #if ticker was not found
            return False

        if int(months[contract[0]]) < 3:
            expirDate = getExpirDate(ticker, contract)
        else:
            if len(contract[1]) == 1:
                contract[1] = '0' + contract[1]
            expirDate = '2020-' + months[contract[0]] + '-' + contract[1]       #correctly format the expiration date

        strike = contract[2]                                                        #set strike
        strikeIndex = 2                                                             #remember the index of the strike

    optionType = strike[-1]       #store contract type

    if optionType == 'P':
        optionType = 'put'
        strike = strike[1:-1]       #remove the $ and the contract type
    elif optionType == 'C':
        optionType = 'call'
        strike = strike[1:-1]       #remove the $ and the contract type
    else:                           #if Josh put a space between the strike and the contract type
        strike = strike[1:]         #remove just the $
        if contract[strikeIndex + 1] == 'C':
            optionType = 'call'
        elif contract[strikeIndex + 1] == 'P':
            optionType = 'put'

    return (ticker, strike, expirDate, optionType)


def getExpirDate(ticker, contract):
    """
    FIND THE EXPIRATION DATE IF HE ONLY PUT THE MONTH AND NOT THE DAY
    """
    month = '-' + months[contract[0]] + '-'
    possibleExpirs = r.get_chains(ticker, info = 'expiration_dates')
    for date in possibleExpirs:
        if month in date:
            return date


months = {
    'JAN': '01',
    'FEB': '02',
    'MAR': '03',
    'MARCH': '03',
    'APR': '04',
    'APRIL': '04',
    'MAY': '05',
    'JUN': '06',
    'JUNE': '06',
    'JUL': '07',
    'JULY':'07',
    'AUG': '08',
    'SEP': '09',
    'SEPT':'09',
    'OCT': '10',
    'NOV': '11',
    'DEC': '12'
}
