import datetime
import pytz


def now_rounded():
    now = datetime.datetime.now(pytz.UTC).replace(second=0, microsecond=0)
    return now
