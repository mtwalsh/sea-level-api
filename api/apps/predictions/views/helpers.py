import datetime

from collections import namedtuple
from itertools import tee, izip
from urlparse import urlparse, urlunparse, parse_qsl
from urllib import urlencode

import pytz

from django.core.exceptions import ObjectDoesNotExist

from api.apps.locations.models import Location
from ..models import Prediction

from .exceptions import InvalidLocationError

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

TimeRange = namedtuple('TimeRange', 'start,end')


class NoStartTimeGivenError(Exception):
    pass


def get_prediction_queryset(location_slug, start_param, end_param):
    try:
        location = Location.objects.get(slug=location_slug)
    except ObjectDoesNotExist:
        raise InvalidLocationError(
            'Invalid location: "{}". See locations endpoint.'.format(
                location_slug))

    try:
        time_range = parse_time_range(start_param, end_param)
    except NoStartTimeGivenError:
        # TODO: Implement list() method and redirect if no start parameter
        # is given. See ListModelMixin
        return Prediction.objects.none()

    queryset = Prediction.objects.filter(
        location=location)

    queryset = queryset.filter(datetime__gte=time_range.start)

    if time_range.end:
        queryset = queryset.filter(datetime__lt=time_range.end)

    return queryset.order_by('datetime')


def parse_time_range(start, end):
    if start is None:
        raise NoStartTimeGivenError()

    start_time = parse_datetime(start)

    if end is None:
        end_time = start_time + datetime.timedelta(hours=6)
    else:
        end_time = parse_datetime(end)

    return TimeRange(start=start_time, end=end_time)


def parse_datetime(datetime_string):
    return datetime.datetime.strptime(
        datetime_string, DATETIME_FORMAT).replace(tzinfo=pytz.UTC)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


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


def add_start_of_now_to_url(url):
    """
    Add eg ?start=2014-05-18T16:45:00Z to a URL
    """
    p = urlparse(url)
    query_params = parse_qsl(p.query)
    query_params.append(('start', get_utc_now_rounded()))

    return urlunparse(
        (p.scheme,
         p.netloc,
         p.path,
         p.params,
         urlencode(query_params),
         p.fragment))


def get_utc_now_rounded():
    now = datetime.datetime.now(pytz.UTC).replace(second=0, microsecond=0)
    return now.strftime(DATETIME_FORMAT)
