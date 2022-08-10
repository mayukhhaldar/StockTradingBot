import sqlite3
from sqlite3 import Error


def get_connection_cursor(db_name):
    con = None
    try:
        con = sqlite3.connect(db_name)
    except Error as e:
        print(e)
    cur = con.cursor()

    return (con, cur)


class SystemDB(object):
    db_path = 'system_databases/system.db'

    def get_num_accounts(self):

        (con, cur) = get_connection_cursor(self.db_path)
        stat_type = 'number_of_accounts'
        cur.execute(
            "SELECT stat_value FROM account_stats WHERE stat_type=?", [stat_type])
        num_accounts = cur.fetchall()
        con.commit()

        return int(num_accounts[0][0])

    def increment_num_accounts(self):

        new_num = self.get_num_accounts() + 1

        (con, cur) = get_connection_cursor(self.db_path)

        stat_type = 'number_of_accounts'
        cur.execute("DELETE FROM account_stats WHERE stat_type=?",
                    (stat_type, ))
        con.commit()

        cur.execute("INSERT INTO account_stats(stat_type, stat_value) VALUES (?, ?)",
                    (stat_type, new_num))
        con.commit()

    def add_account(self, full_name, username, password, account_id, key_id, secret_id):
        name = full_name.lower()
   
        (con, cur) = get_connection_cursor(self.db_path)
        try:
            cur.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?)",
                        (account_id, name, username, key_id, secret_id))
            con.commit()
        except:
            print("Was not able to insert into accounts database")

        try:
            cur.execute("INSERT INTO account_login VALUES (?, ?, ?)",
                        (username, password, account_id))
            con.commit()
        except:
            print("Was not able to insert into accounts_login database")

    def remove_account(self, account_id):
        (con, cur) = get_connection_cursor(self.db_path)
        cur.execute("DELETE FROM accounts WHERE account_id=?", (account_id,))
        con.commit()
        cur.execute("DELETE FROM account_login WHERE account_id=?",
                    (account_id,))

    def get_specifc_account(self, account_id):
        (con, cur) = get_connection_cursor(self.db_path)
        cur.execute("SELECT * FROM accounts WHERE account_id=?", (account_id,))
        account_info = cur.fetchone()
        con.commit()
        return account_info

    def update_name(self, new_name, account_id):
        (con, cur) = get_connection_cursor(self.db_path)
        new_name.lower()
        cur.execute("UPDATE accounts SET name=? WHERE account_id=?",
                    (new_name, account_id,))
        con.commit()

    def update_api_keys(self, key_id, secret_id, account_id):
        (con, cur) = get_connection_cursor(self.db_path)
        cur.execute("UPDATE accounts SET key_id=?, secret_id=? WHERE account_id=?",
                    (key_id, secret_id, account_id,))
        con.commit()

    def get_account_id(self, username, password):
        (con, cur) = get_connection_cursor(self.db_path)
        cur.execute(
            "SELECT account_id FROM account_login WHERE username=? AND password=?", (username, password,))
        account_id = cur.fetchone()
        con.commit()
        return int(account_id[0])

    def get_account_list(self):
        (con, cur) = get_connection_cursor(self.db_path)
        cur.execute('SELECT * FROM accounts')
        accounts = cur.fetchall()
        con.commit()
        return accounts

    def print_account_list(self):
        (con, cur) = get_connection_cursor(self.db_path)
        for row in cur.execute('SELECT * FROM accounts'):
            print(row)
        con.commit()
