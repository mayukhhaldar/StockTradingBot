'''
Rules for algorithm design:

Algorithms have full flexibility in input parameters,
however the output should have a list of the order, each order will have the 
[type of order, quanitity, symbol]
'''


#Some very simple algorithms for starting

def constant_threshold(account):
    buy_threshold = 50
    sell_threshold = -10

    orders = []

    #if any return crosses the threshold window, sell or buy accordingly
    for position in account.positions:
        total_pl = float(position.unrealized_pl)
        
        if total_pl > buy_threshold or total_pl < sell_threshold:
            order = ('sell', position.qty, position.symbol)
            orders.append(order)

    return orders

def recurisve_constant_threshold(account):
    NotImplemented

""" This martingale strategy works on a time interval basis on a stock:
    - First select a stock 



"""
def martingale():
    NotImplemented

def mean_reversion():
    NotImplemented

def moving_average_crossover():
    NotImplemented

def long_short():
    NotImplemented