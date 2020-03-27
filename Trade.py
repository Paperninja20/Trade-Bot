import time
import robin_stocks as r

#FUNCTION TO GET THE OPTIMAL AMOUNT OF CONTRACTS
def OptimalContracts(bp, ask):
    optimal = int(bp/ask)
    if optimal > 100:       #Maximum purchasable contracts is 100
        optimal = 100
    return optimal

#FUNCTION TO BUY
def getIn(symbol, price, quantity, expirationDate, strike, type):
    print(r.order_buy_option_limit('open', 'debit', price, symbol, quantity, expirationDate, strike, optionType = type, timeInForce = 'gfd'))   #buy the contracts
    print('\nBOUGHT')
    print(str(quantity), end = ' ')
    print(expirationDate, end = ' ')
    print(symbol, end = ' $')
    print(strike, end = ' ')
    print(type, end = 's at $')
    print(str(price))
    return price * quantity

#FUNCTION TO SELL
def getOut(symbol, price, quantity, expirationDate, strike, type):
    print(r.order_sell_option_limit('close', 'debit', price, symbol, quantity, expirationDate, strike, optionType = type, timeInForce = 'gfd'))  #sell the contracts
    print('SOLD')
    print(str(quantity), end = ' ')
    print(expirationDate, end = ' ')
    print(symbol, end = ' $')
    print(strike, end = ' ')
    print(type, end = 's at $')
    print(str(price))
    return price * quantity

#MAIN FUNCTION
def bank(symbol, expirationDate, strike, optionType):
    bp = float(r.load_account_profile('buying_power'))                                                              #get buying power
    ask = int(float(r.get_option_market_data(symbol, expirationDate, strike, optionType, info = "ask_price")) * 100)     #get the ask of the contract
    bid = int(float(r.get_option_market_data(symbol, expirationDate, strike, optionType, info = "bid_price")) * 100)     #get the bid of the contract
    market = int(float(r.get_option_market_data(symbol, expirationDate, strike, optionType, info = "adjusted_mark_price")) * 100)

    if ask - bid > 30:                                                                  #protect against wide spreads
        quantity = OptimalContracts(bp, market)                                                                            #calculate optimal amount of contracts
        buy = getIn(symbol, market, quantity, expirationDate, strike, optionType)
        print('')
        time.sleep(60)      #wait 45 seconds
        r.cancel_all_open_orders()
        sell = getOut(symbol, ask, quantity, expirationDate, strike, optionType)
        print('')
        if sell - buy >= 0:
            print("Potential PROFIT: $" + str(sell - buy))
        else:
            print("Potential PROFIT: -$" + str(-1 * (sell - buy)))
        print('')
    else:
        quantity = OptimalContracts(bp, ask)                                                                            #calculate optimal amount of contracts
        buy = getIn(symbol, ask, quantity, expirationDate, strike, optionType)
        print('')
        time.sleep(60)      #wait 45 seconds
        r.cancel_all_open_orders()
        sell = getOut(symbol, market, quantity, expirationDate, strike, optionType)
        print('')
        if sell - buy >= 0:
            print("Potential PROFIT: $" + str(sell - buy))
        else:
            print("Potential PROFIT: -$" + str(-1 * (sell - buy)))
        print('')
