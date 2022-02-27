from database import SystemDB
from account_setup import run_ui
from system_run import system_startup, run


def system_control():

    # getting all user accounts setup
    run_ui()

    # getting all active accounts and setting up their databases and algorithms
    system_startup()

    auto = False

    while True:
        run()
        if not auto:
            break


if __name__ == "__main__":
    system_control()
