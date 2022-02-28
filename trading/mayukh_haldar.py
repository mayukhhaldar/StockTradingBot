import pandas_datareader.data as web
import pandas_datareader as pdr
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np


'''
IF SMA(SHORT PERIOD) > SMA(LONG PERIOD) => BUY
IF SMA(LONG PERIOD) > SMA(SHORT PERIOD) => SELL

'''


def sma_crossover(symbol):

    now = datetime.now()

    current_date = now.strftime("%d/%m/%Y %H:%M:%S")

    asset = pdr.get_data_yahoo(symbol,
                               start=datetime(2010, 12, 20),
                               end=current_date)

    small_window = 50
    large_window = 100

    signals = pd.DataFrame(index=asset.index)
    signals['signal'] = 0.0

    signals['small_sma'] = asset['Close'].rolling(
        window=small_window, min_periods=1, center=False).mean()

    signals['large_sma'] = asset['Close'].rolling(
        window=large_window, min_periods=1, center=False).mean()

    # True means buy, False means sell
    signals['signal'] = np.where(signals['small_sma']
                                 > signals['large_sma'], True, False)

    signal = signals.iloc[-1]['signal']
    limit = signals.iloc[-1]['large_sma']

    # During the sell and buy use limit orders,
    # limit should be the restricting price
    if signal:
        # Buy the stock or keep it
        return ('buy', limit)
    else:
        # sell stock
        return ('sell', limit)


def feasibility_check(cash, quantity, limit):
    return (quantity*limit) < (cash - 10000)

# Remember to change to execute
def mayukh_haldar(alpaca_account):

    watchlist = ['AAPL', 'JPM', 'AMZN', 'AXP', 'PFE', 'VZ', 'GM', 'GE']

    stocks = alpaca_account.get_positions()
    symbols = alpaca_account.get_symbol_list()
    orders = alpaca_account.orders
    in_order = []
    
    for order in orders:
        in_order.append(order.symbol)

    for symbol in watchlist:

        if symbol in in_order:
            continue
        else:
            (decision, limit) = sma_crossover(symbol)

            if symbol in symbols:
                if decision == 'sell':
                    alpaca_account.execute_limit_sell(
                        symbol, stocks[symbol][0], limit)
            else:
                if decision == 'buy':
                    quantity = 5
                    if feasibility_check(float(alpaca_account.get_account_cash()), quantity, limit):
                        alpaca_account.execute_limit_buy(symbol, quantity, limit)
