from database import SystemDB, get_connection_cursor
import os

'''
This script should not be modified and is not be imported into application.
It is to be used only for setting up the inital values in the databases
so the application can pull the information and get started.

'''

db_path = 'system_databases/system.db'


def create_system_databases(db_path):

    (con, cur) = get_connection_cursor(db_path)

    account_stats = True
    accounts = True
    login = True
    trades = True

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS account_stats
                    (stat_type TEXT PRIMARY KEY, stat_value INTEGER)''')
        con.commit()
        account_stats = True
    except:
        account_stats = False

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS account_login
                        (username TEXT, password TEXT, account_id INTEGER, PRIMARY KEY(username, password))''')
        con.commit()
        login = True
    except:
        login = False

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS accounts
                    (account_id INTEGER PRIMARY KEY, account_name TEXT, username TEXT, key_id TEXT UNIQUE, secret_id TEXT UNIQUE)''')
        con.commit()
        accounts = True
    except:
        accounts = False

    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS trades_log
                    (account_id INTEGER, symbol TEXT, quantity INTEGER, side TEXT, type TEXT, limit_price TEXT)''')
        con.commit()
        return True
    except:
        return False

    if accounts and account_stats and login and trades:
        return True
    else:
        return False


# This function usually should never be called
def close_databases():
    (con, cur) = get_connection_cursor(db_path)
    cur.execute('''DROP TABLE IF EXISTS account_stats''')
    con.commit()
    cur.execute('''DROP TABLE IF EXISTS accounts''')
    cur.execute('''DROP TABLE IF EXISTS account_login''')
    cur.execute('''DROP TABLE IF EXISTS trades_log''')
    os.remove("system_databases/system.db")


def set_num_accounts(number):

    (con, cur) = get_connection_cursor(db_path)

    stat_type = 'number_of_accounts'

    cur.execute("DELETE FROM account_stats WHERE stat_type=?",
                (stat_type, ))
    con.commit()

    cur.execute("INSERT INTO account_stats(stat_type, stat_value) VALUES (?, ?)",
                (stat_type, number))
    con.commit()


def intialize_num_accounts():

    (con, cur) = get_connection_cursor(db_path)

    stat_type = "number_of_accounts"
    stat_value = 0

    cur.execute("INSERT INTO account_stats(stat_type, stat_value) VALUES (?, ?)",
                (stat_type, stat_value))
    con.commit()


def get_num_accounts():

    (con, cur) = get_connection_cursor(db_path)
    stat_type = 'number_of_accounts'
    cur.execute(
        "SELECT stat_value FROM account_stats WHERE stat_type=?", [stat_type])
    num_accounts = cur.fetchall()
    con.commit()

    return int(num_accounts[0][0])


# These functions should be the ones called
def initialize_system_database():
    db_path = 'system_databases/system.db'
    return create_system_databases(db_path)

# --------------------------------------------------------------------------------------------
# should only be called once to start the system or after a hard restart of the system


def system_database_full_startup():
    close_databases()
    if not initialize_system_database():
        print("Failed to initalize systems databases")
    intialize_num_accounts()
    print(get_num_accounts())


def system_database_force_shutdown():
    # function should have some sort of protection
    close_databases()


def system_database_hard_restart():

    close_databases()
    initialize_system_database()
    intialize_num_accounts()
    print("System has been restarted")


# --------------------------------------------------------------------------------------------
# Write any required admin code over here

# This restarts the entire database systems
# Be careful, if this script is run then it will erase all saved information (including account information)
system_database_hard_restart()
