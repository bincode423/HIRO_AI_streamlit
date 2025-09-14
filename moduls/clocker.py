from datetime import datetime

def get_datetime_string():
    now = datetime.now()
    return now.strftime("%Y/%m/%d/%H/%M/%S")

def clock_class():
    return datetime.now()