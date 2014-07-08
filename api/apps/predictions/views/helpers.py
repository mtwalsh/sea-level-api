import datetime

from collections import namedtuple
from itertools import tee

try:
    from itertools import izip as zip  # On 2, replace zip with izip
except ImportError:
    pass  # Python 3 has zip already

import pytz

from django.core.exceptions import ObjectDoesNotExist

from api.apps.locations.models import Location
from ..models import Prediction

from .exceptions import (InvalidLocationError, NoStartTimeGivenError,
                         NoEndTimeGivenError)

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

TimeRange = namedtuple('TimeRange', 'start,end')


def parse_and_get_queryset(location_slug, start_param, end_param):
    location = parse_location(location_slug)
    time_range = parse_time_range(start_param, end_param)
    return get_queryset(location, time_range)


def get_queryset(location, time_range):
    queryset = Prediction.objects.filter(
        location=location,
        datetime__gte=time_range.start,
        datetime__lt=time_range.end)

    return queryset.order_by('datetime')


def parse_location(location_slug):
    """
    From a location slug ie 'liverpool-gladstone-dock', return a Location model
    object or blow up with an appropriate API Exception.
    """
    if location_slug is None:
        raise InvalidLocationError(
            'No location given, see locations endpoint.')

    try:
        location = Location.objects.get(slug=location_slug)
    except ObjectDoesNotExist:
        raise InvalidLocationError(
            'Invalid location: "{}". See locations endpoint.'.format(
                location_slug))
    return location


def parse_time_range(start, end):
    if start is None:
        raise NoStartTimeGivenError()

    if end is None:
        raise NoEndTimeGivenError()

    return TimeRange(start=parse_datetime(start), end=parse_datetime(end))


def parse_datetime(datetime_string):
    return datetime.datetime.strptime(
        datetime_string, DATETIME_FORMAT).replace(tzinfo=pytz.UTC)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def split_prediction_windows(predictions):
    """
    `predictions` contains all the times for which the tide is above a certain
    level, eg, if there are two tidal windows, it will contain every minutely
    prediction for the first, followed by every prediction for the second.

    This function yield the start and end prediction of each time window:
    based on discontinuities in time (ie a gap larger than one minue)

    a0, a1, a2, a3, a0, b0, b1, b2, b3  => (a0, a3), (b0, b3)
    """
    def _remove_unequal(pair):
        return pair[0] != pair[1]

    return filter(
        _remove_unequal,
        _split_prediction_windows_unfiltered(predictions)
    )


def _split_prediction_windows_unfiltered(predictions):
    if not len(predictions):
        return

    one_minute = datetime.timedelta(seconds=60)

    window_start = predictions[0]
    last_prediction_seen = None

    for p0, p1 in pairwise(predictions):
        timediff = p1.datetime - p0.datetime

        if timediff > one_minute:
            yield window_start, p0
            window_start = p1

        elif p0.datetime >= p1.datetime:
            raise ValueError("Predictions must be ordered and ascending.")

        last_prediction_seen = p1

    yield window_start, last_prediction_seen


def now_rounded():
    now = datetime.datetime.now(pytz.UTC).replace(second=0, microsecond=0)
    return now


def format_datetime(dt):
    """
    >>> format_datetime(datetime.datetime(2014, 5, 3, 13, 4, 0,\
                                          tzinfo=pytz.UTC))
    '2014-05-03T13:04:00Z'
    """
    assert dt.tzinfo is not None, dt
    return dt.strftime(DATETIME_FORMAT)
