from database import SystemDB, get_connection_cursor
from trading import bot_index
from trading.trading_support import TradingBot_Account


''' 
This basically extracts all the user information from the database and then creates their trading bot objects

'''

def system_startup():
    list_accounts = SystemDB().get_account_list()

    for account in list_accounts:
        account_id = account[0]
        full_name = account[1]
        username = account[2]
        key_id =  account[3]
        secret_id = account[4]

        bot_index.append(TradingBot_Account(account_id, full_name, username, key_id, secret_id)) 


def clear_bot_list():
    bot_index.clear()

def run():
    for account in bot_index:
        account.run_algorithm()
        