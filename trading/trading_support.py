from trading import algorithm_dictionary
from trading.trades_log import add_trades
import alpaca_trade_api as tradeapi


class Alpaca_Account(object):
    def __init__(self, account_id, key_id, secret_id):
        self.account_id = account_id
        self.key = key_id
        self.secret = secret_id
        self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
        self.api = tradeapi.REST(self.key, self.secret, self.alpaca_endpoint)
        self.account = self.api.get_account()
        self.positions = self.api.list_positions()
        self.portfolio_return = self.get_portfolio_return()

    # get the cash balance of the account
    def get_account_cash(self):
        return self.account.cash

    # See the special configurations of the account
    def get_account_configurations(self):
        print(self.api.get_account_configurations())

    # See what orders are currently placed
    def get_order_list(self):
        order_list = self.api.list_orders()
        for order in order_list:
            print(order.side + " " + order.qty + " shares of " + order.symbol)

    # buy the stock
    def execute_buy(self, ticker, quantity):
        try:
            add_trades(self.account_id, ticker,
                       quantity, "buy", "market", str(0))
            self.api.submit_order(ticker, quantity)
        except:
            print("Could not place order")

    def execute_sell(self, ticker, quantity):
        try:
            add_trades(self.account_id, ticker, quantity,
                       "sell", "market", str(0))
            self.api.submit_order(ticker, quantity, "sell")
        except:
            print("Could not place order")

    def execute_limit_buy(self, ticker, quantity, limit):
        try:
            #self.api.submit_order(ticker, quantity, "buy", type='limit', limit_price=str(limit))
            add_trades(self.account_id, ticker, quantity,
                       "buy", "limit", str(limit))
            print("We are buying " + ticker + " at " + str(limit))
        except:
            print("Could not place order")

    def execute_limit_sell(self, ticker, quantity, limit):
        try:
            #self.api.submit_order(ticker, quantity, "sell", limit_price=limit)
            add_trades(self.account_id, ticker, quantity,
                       "sell", "limit", str(limit))
            print("We are selling " + ticker + " at " + str(limit))
        except:
            print("Could not place order")

    def get_positions(self):
        positions = self.api.list_positions()

        position_dict = {}

        for position in positions:
            position_dict[position.symbol] = (
                position.qty, position.side, position.current_price)

        return position_dict

    def get_symbol_list(self):

        positions = self.api.list_positions()

        symbol_list = []

        for position in positions:
            symbol_list.append(position.symbol)

        return symbol_list

    def get_portfolio_return(self):
        initial = 100000
        current = float(self.account.equity)
        return ((current - initial)/initial)*100

    def daily_summary(self):
        # This will be given out as a report
        print("Today's Performance($): ")

        for position in self.positions:
            print("\t" + position.symbol + ": " +
                  position.unrealized_intraday_pl)

        print("\nOverall Performance($): ")

        for position in self.positions:
            print("\t" + position.symbol + ": " + position.unrealized_pl)

        print("\nPortfolio Return: " + str(self.get_portfolio_return()) + "%")


class TradingBot_Account(object):
    def __init__(self, account_id, full_name, username, key_id, secret_id):
        self.account_id = account_id
        self.name = full_name
        self.username = username
        self.portfolio_path = 'account_databases/' + \
            str(self.account_id) + "_" + self.username
        self.account = Alpaca_Account(account_id, key_id, secret_id)

    def run_algorithm(self):
        algorithm_dictionary[str(self.account_id)](self.account)
