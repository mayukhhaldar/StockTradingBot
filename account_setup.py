from database import SystemDB
from getpass import getpass

def add_account():

    # get the account information from the user
    full_name = input("Please enter your full name: ")
    key_id = input("Please enter your Key_ID: ")
    secret_id = input("Please enter your Secret_ID: ")

    review = "Full Name: " + full_name + "\nKey_ID: " + \
        key_id + "\nSecret_ID: " + secret_id

    (username, password) = fetch_credentials()

    print(review)
    response = input("Confirm this account will be added (y/n)")

    if response == "y":
        system_db = SystemDB()
        account_id = generate_account_id(system_db)
        try:
            system_db.add_account(full_name, username,
                                  password, account_id, key_id, secret_id)
        except:
            print("Add account failed")
        else:
            print("Account has be added, here is the information and your Account ID")
            print(system_db.get_specifc_account(account_id))


def delete_account(account_id):
    response = input("Are you sure you want to delete your account? (y/n)")
    if response == "y":
        system_db = SystemDB()
        try:
            system_db.remove_account(account_id)
        except:
            print("Account deletion failed")
        else:
            print("Account deleted")


def modify_account(account_id):
    response = input("What would you like to modify\n1. Name\n2.API Keys?")
    system_db = SystemDB()

    if response == "Name":
        name = input("Please enter the new name:")
        system_db.update_name(name, account_id)
    elif response == "API Keys":
        key_id = input("Please enter your key id:")
        secret_id = input("Please enter your secret id:")
        system_db.update_api_keys(key_id, secret_id, account_id)


# Current logic is to increment by one, may want to encode later on
def generate_account_id(system_db):
    return system_db.get_num_accounts() + 1


def fetch_credentials():
    username = input("Please enter your username: ")

    password = None
    password_incorrect = True

    while password_incorrect:
        password = getpass("Please enter your password: ")
        if password != getpass("Please re-enter your password: "):
            password_incorrect = True
        else:
            password_incorrect = False

    return (username, password)


def login_options(account_id):
    print("What would you like to do?")
    print("1. Modify Account" +
          "\n2. Delete Account" +
          "\n3. Get Account ID")

    resp = input("What would you like to do? (1/2)")

    if resp == "1":
        modify_account(account_id)
    elif resp == "2":
        delete_account(account_id)
    elif resp == "3":
        (username, password) = fetch_credentials()
        print(SystemDB().get_account_id(username, password))


def login():
    username = input("Please enter your username: ")
    print("Please enter your password")
    password = getpass()

    system_db = SystemDB()
    try:
        account_id = system_db.get_account_id(username, password)
    except:
        print("Account not found")
    else:
        return account_id


def test_script(add):
    key = 'PKIRXLKY0R69F4OF4T1P'
    secret = 'eUa5dXSzL1voDnCty4ug7ZlfbAESUZNi53v0n4DS'

    system_db = SystemDB()
    account_id = generate_account_id(system_db)
    full_name = "Mayukh Haldar"
    username = "mayukhhaldar"
    password = "trial"

    if add:
        system_db.add_account(full_name, username,
                              password, account_id, key, secret)
    system_db.print_account_list()
    system_db.get_account_login_details()


def run_ui():
    print("Would you like to login or add an account?")
    response = input(
        "1. Login\n2. Add Account\n3. Exit\n4. Continue to program\n5. Run Test Script\n(1/2/3/4):")

    if response == "1":
        login_options(login())
    elif response == "2":
        add_account()
    elif response == "3":
        exit()
    elif response == "4":
        return
    elif response == "5":
        test_script(True)
