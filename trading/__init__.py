from trading.default_algorithm import default_algorithm

# map should contain list of TradingBot_Accounts

bot_index = []

#define an algorithm dictionary
# the key is the account_id and the value is the corresponding function

algorithm_dictionary = {
    '1': default_algorithm,
}


