from datetime import datetime
import time

def is_same_day(timestamp1, timestamp2):
    dt1 = datetime.fromtimestamp(timestamp1)
    dt2 = datetime.fromtimestamp(timestamp2)

    return dt1.year == dt2.year and dt1.month == dt2.month and dt1.day == dt2.day

def second()->int:
    return int(time.time())

