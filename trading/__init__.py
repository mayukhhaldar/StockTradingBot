from trading.mayukh_haldar import mayukh_haldar

# map should contain list of TradingBot_Accounts

bot_index = []

#define an algorithm dictionary
# the key is the account_id and the value is the corresponding function

algorithm_dictionary = {
    '1': mayukh_haldar,
}


