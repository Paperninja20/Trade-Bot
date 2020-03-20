import Config
import click
import time
import robin_stocks as r

logged_in = r.login(username = Config.USERNAME, password = Config.PASSWORD, store_session = True)   #login

#FUNCTION TO GET THE OPTIMAL AMOUNT OF CONTRACTS
def OptimalContracts(bp, ask):
    optimal = int(bp/ask)
    if optimal > 100:       #Maximum purchasable contracts is 100
        optimal = 100
    return optimal

#FUNCTION TO BUY
def getIn(symbol, price, quantity, expirationDate, strike, type):
    r.order_buy_option_limit("open", price, symbol, quantity, expirationDate, strike, optionType = type, timeInForce = 'gfd')   #buy the contracts
    print('\nBOUGHT')
    print(str(quantity), end = ' ')
    print(expirationDate, end = ' ')
    print(symbol, end = ' $')
    print(strike, end = ' ')
    print(type, end = 's at ')
    print(str(price))
    return price * quantity

#FUNCTION TO SELL
def getOut(symbol, price, quantity, expirationDate, strike, type):
    r.order_sell_option_limit("close", price, symbol, quantity, expirationDate, strike, optionType = type, timeInForce = 'gfd') #sell the contracts
    print('SOLD')
    print(str(quantity), end = ' ')
    print(expirationDate, end = ' ')
    print(symbol, end = ' $')
    print(strike, end = ' ')
    print(type, end = 's at ')
    print(str(price))
    return price * quantity

#MAIN FUNCTION
def bank(symbol, expirationDate, strike, optionType):
    bp = float(r.load_account_profile('buying_power'))                                                              #get buying power
    ask = float(r.get_option_market_data(symbol, expirationDate, strike, optionType, info = "ask_price")) * 100     #get the ask of the contract
    bid = float(r.get_option_market_data(symbol, expirationDate, strike, optionType, info = "bid_price")) * 100     #get the bid of the contract
    quantity = OptimalContracts(bp, ask)                                                                            #calculate optimal amount of contracts

    if ask - bid > 30:                                                                  #protect against wide spreads
        buy = getIn(symbol, bid, quantity, expirationDate, strike, optionType)
        print('')
        time.sleep(45)      #wait 45 seconds
        sell = getOut(symbol, ask, quantity, expirationDate, strike, optionType)
        print('')
        print("PROFIT: " + str(sell - buy))
        print('')
    else:
        buy = getIn(symbol, ask, quantity, expirationDate, strike, optionType)
        print('')
        time.sleep(45)      #wait 45 seconds
        sell = getOut(symbol, bid, quantity, expirationDate, strike, optionType)
        print('')
        print("PROFIT: " + str(sell - buy))
        print('')
