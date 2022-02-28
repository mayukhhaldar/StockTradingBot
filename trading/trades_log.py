import sqlite3
from sqlite3 import Error

db_path = "system_databases/system.db"


def get_connection_cursor(db_name):
    con = None
    try:
        con = sqlite3.connect(db_name)
    except Error as e:
        print(e)
    cur = con.cursor()

    return (con, cur)


def add_trades(account_id, symbol, quantity, side, order_type, price):
    (con, cur) = get_connection_cursor(db_path)
    cur.execute("INSERT INTO trades_log VALUES (?, ?, ?, ?, ?, ?)",
                (account_id, symbol, quantity, side, order_type, price))
    con.commit()


def get_trades():
    (con, cur) = get_connection_cursor(db_path)
    cur.execute('SELECT * FROM trades_log')
    print(cur.fetchall())
    con.commit()


def get_trades_for_account(account_id):
    (con, cur) = get_connection_cursor(db_path)
    cur.execute("SELECT * FROM trades_log WHERE account_id=?", (account_id,))
    trades = cur.fetchall()
    con.commit()
    print(trades)
