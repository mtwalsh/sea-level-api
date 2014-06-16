import datetime

from collections import namedtuple

from urlparse import urlparse, urlunparse, parse_qsl
from urllib import urlencode

import pytz

from rest_framework.generics import ListAPIView

from api.apps.locations.models import Location
from api.libs.json_envelope_renderer import replace_json_renderer

from ..models import Prediction
from ..serializers import TideLevelSerializer

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

TimeRange = namedtuple('TimeRange', 'start,end')


class NoStartTimeGivenError(Exception):
    pass


class TideLevels(ListAPIView):
    """
    Get tidal predictions at a given location. Valid parameters are
    `start` and `end` (in format `2014-05-01T00:17:00Z`)
    """
    renderer_classes = replace_json_renderer(ListAPIView.renderer_classes)
    model = Prediction
    serializer_class = TideLevelSerializer

    def get_queryset(self):
        location_slug = self.kwargs['location_slug']
        location = Location.objects.get(slug=location_slug)  # TODO: catch 404

        try:
            time_range = parse_time_range(self.request.QUERY_PARAMS)
        except NoStartTimeGivenError:
            # TODO: Implement list() method and redirect if no start parameter
            # is given. See ListModelMixin

            return Prediction.objects.none()

        queryset = Prediction.objects.filter(
            location=location)

        if time_range.start:
            queryset = queryset.filter(datetime__gte=time_range.start)

        if time_range.end:
            queryset = queryset.filter(datetime__lt=time_range.end)

        return queryset.order_by('datetime')[:60]  # limit to 60


def parse_time_range(query_params):
    start = query_params.get('start', None)
    end = query_params.get('end', None)

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
