import time
import datetime
import holidays


def wait_till_market_open():
    weekno = datetime.datetime.today().weekday()
    current_time = datetime.datetime.now()
    current_date = datetime.date.today()

    usa_holidays = holidays.UnitedStates()

    holiday = current_date in usa_holidays

    market_open = current_time.replace(
        hour=9, minute=30, second=0, microsecond=0)
    market_close = current_time.replace(
        hour=16, minute=0, second=0, microsecond=0)

    if not holiday and weekno < 5:
        if market_open > current_time:
            print("Will wake up at:", market_open)
            time_to_open = (market_open - current_time).total_seconds()
            print("Going to sleep for:", time_to_open)
            time.sleep(time_to_open)
        elif market_close > current_time:
            print("Market Open")
        else:
            market_open += datetime.timedelta(days=1)
            print("Will wake up at:", market_open)
            time_to_open = (market_open - current_time).total_seconds()
            print("Going to sleep for:", time_to_open)
            time.sleep(time_to_open)
    else:
        working_day = False
        while not working_day:
            market_open += datetime.timedelta(days=1)
            print(market_open)
            weekno = market_open.weekday()
            if weekno < 5 and not market_open in usa_holidays:
                working_day = True
                print("Will wake up at:", market_open)
                time_to_open = (market_open - current_time).total_seconds()
                print("Going to sleep for:", time_to_open)
                time.sleep(time_to_open)
