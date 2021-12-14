import alpaca_trade_api as tradeapi
import pandas as pd

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

    def get_account_configurations(self):
        print(self.api.get_account_configurations())

    def get_order_list(self):
        order_list = self.api.list_orders()
        for order in order_list:
            print(order.side + " " + order.qty + " shares of " + order.symbol)

    def execute_buy(self, ticker, quantity):
        self.api.submit_order(ticker, quantity)

    def execute_sell(self, ticker, quantity):
        self.api.submit_order(ticker, quantity, "sell")
    
    def summarise_positions(self):
        print(self.api.list_positions())

    def get_positions(self):
        return self.api.list_positions()

    def get_portfolio_return(self):
        initial = 100000
        current = float(self.account.equity)
        return ((current - initial)/initial)*100

    def get_account_summary(self):
        NotImplemented

    def daily_summary(self):
        NotImplemented
        # Should give the daily profit and loss for every stock





