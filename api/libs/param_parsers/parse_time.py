import datetime

from collections import namedtuple
from itertools import tee

try:
    from itertools import izip as zip  # On 2, replace zip with izip
except ImportError:
    pass  # Python 3 has zip already

import pytz

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from api.apps.locations.models import Location

from .exceptions import (InvalidLocationError, NoStartTimeGivenError,
                         NoEndTimeGivenError)

TimeRange = namedtuple('TimeRange', 'start,end')


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
        datetime_string, settings.DATETIME_FORMAT).replace(tzinfo=pytz.UTC)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
