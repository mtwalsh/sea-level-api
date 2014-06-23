import datetime

from collections import namedtuple
from urlparse import urlparse, urlunparse, parse_qsl
from urllib import urlencode

import pytz

from api.apps.locations.models import Location
from ..models import Prediction

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

TimeRange = namedtuple('TimeRange', 'start,end')


class NoStartTimeGivenError(Exception):
    pass


def get_prediction_queryset(location_slug, start_param, end_param):
    location = Location.objects.get(slug=location_slug)  # TODO: catch 404

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
