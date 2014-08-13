from django.conf import settings


def format_datetime(dt):
    """
    >>> format_datetime(datetime.datetime(2014, 5, 3, 13, 4, 0,\
                                          tzinfo=pytz.UTC))
    '2014-05-03T13:04:00Z'
    """
    assert dt.tzinfo is not None, dt
    return dt.strftime(settings.DATETIME_FORMAT)
