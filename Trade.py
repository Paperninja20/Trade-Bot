import Config
import click
import time
import robin_stocks as r

logged_in = r.authentication.login(username = Config.USERNAME, password = Config.PASSWORD, store_session = True)

def OptimalContracts(bp, ask):
    optimal = int(bp/ask)
    if optimal > 100:
        optimal = 100
    return optimal

def getIn(symbol, price, quantity, expirationDate, strike, type):
    '''r.order_buy_option_limit("open", price, symbol, quantity, expirationDate, strike, optionType = type, timeInForce = 'gfd')'''
    print('\nBOUGHT')
    print('quantity: ' + str(quantity))
    print('symbol: ' + symbol)
    print('expiration: ' + expirationDate)
    print('strike: ' + strike)
    print('type: ' + type)
    print('price per contract: ' + str(price))
    print('total equity: ' + str(price * quantity))
    return price * quantity

def getOut(symbol, price, quantity, expirationDate, strike, type):
    '''r.order_sell_option_limit("close", price, symbol, quantity, expirationDate, strike, optionType = type, timeInForce = 'gfd')'''
    print('SOLD')
    print('quantity: ' + str(quantity))
    print('symbol: ' + symbol)
    print('expiration: ' + expirationDate)
    print('strike: ' + strike)
    print('type: ' + type)
    print('price per contract: ' + str(price))
    print('new equity: ' + str(price * quantity))
    return price * quantity

def bank(symbol, expirationDate, strike, optionType):
    print(r.options.get_chains(symbol, info = 'expiration_dates'))
    bp = float(r.load_account_profile('buying_power'))
    ask = float(r.get_option_market_data(symbol, expirationDate, strike, optionType, info = "ask_price")) * 100
    bid = float(r.get_option_market_data(symbol, expirationDate, strike, optionType, info = "bid_price")) * 100
    quantity = OptimalContracts(bp, ask)
    buy = getIn(symbol, ask, quantity, expirationDate, strike, optionType)
    print('\n')
    time.sleep(5)
    sell = getOut(symbol, bid, quantity, expirationDate, strike, optionType)
    print('\n')
    print("profit: " + str(sell - buy))
