from account import Alpaca_Account
from algorithms import *

#implement a daily algorithm here and a user interface that allows selling and buying of stocks
def connect() -> Alpaca_Account:
    key = 'PKIRXLKY0R69F4OF4T1P'
    secret = 'eUa5dXSzL1voDnCty4ug7ZlfbAESUZNi53v0n4DS'

    return Alpaca_Account(key, secret)

def control():
    account = connect()

    """ for position in account.get_positions():
        print(position) """
    print(constant_threshold(account))
    #print(account.portfolio_return)
    #account.summarise_positions()


    #algorithms should give a recomendation of moves

    #trading software should take the recomendation and execute the trades
    


control()



