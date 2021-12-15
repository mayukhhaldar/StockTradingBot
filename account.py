import alpaca_trade_api as tradeapi
import pandas as pd
import smtplib

class Alpaca_Account(object):
    def __init__(self, key_id, secret_id):
        self.key = key_id
        self.secret = secret_id
        self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
        self.api = tradeapi.REST(self.key , self.secret, self.alpaca_endpoint)
        self.account = self.api.get_account()
        self.positions = self.api.list_positions()
        self.portfolio_return = self.get_portfolio_return()

    #get the cash balance of the account
    def get_account_cash(self):
        print("The account balance is: $" + self.account.cash)

    #See the special configurations of the account
    def get_account_configurations(self):
        print(self.api.get_account_configurations())

    #See what orders are currently placed 
    def get_order_list(self):
        order_list = self.api.list_orders()
        for order in order_list:
            print(order.side + " " + order.qty + " shares of " + order.symbol)

    #buy the stock
    def execute_buy(self, ticker, quantity):
        self.api.submit_order(ticker, quantity)

    #
    def execute_sell(self, ticker, quantity):
        self.api.submit_order(ticker, quantity, "sell")
    
    def summarise_positions(self):
        NotImplemented


    def get_positions(self):
        return self.api.list_positions()

    def get_portfolio_return(self):
        initial = 100000
        current = float(self.account.equity)
        return ((current - initial)/initial)*100

    def daily_summary(self):
        #This will be given out as a report
        print("Today's Performance($): ")

        for position in self.positions:
            print("\t" + position.symbol + ": " + position.unrealized_intraday_pl)

        print("\nOverall Performance($): ")

        for position in self.positions:
            print("\t" + position.symbol + ": " + position.unrealized_pl)

        print("\nPortfolio Return: " + str(self.get_portfolio_return()) + "%")

    def execution(self, trade_recomendations):
        #Take the list of recomended trades and execute them 
        NotImplemented





