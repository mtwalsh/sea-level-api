from .exceptions import InvalidParameterError


def parse_interval(interval_string):
    try:
        interval_mins = int(interval_string)
    except ValueError:
        raise InvalidParameterError(
            "Invalid interval: expected integer (minutes)")

    if not 1 <= interval_mins <= 60:
        raise InvalidParameterError(
            'Invalid interval: must be between 1 and 60 minutes')

    return interval_mins
