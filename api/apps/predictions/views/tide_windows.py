import datetime

from functools import partial

try:
    # Python 2: use iterator versions
    from itertools import imap as map
    from itertools import ifilter as filter
except ImportError:
    pass

from rest_framework.generics import ListAPIView

from api.libs.json_envelope_renderer import replace_json_renderer
from api.libs.param_parsers import (parse_location, parse_time_range,
                                    parse_tide_level)

from ..serializers import TideWindowSerializer

from .helpers import (get_queryset, split_predictions_into_tide_windows,
                      TimeRange)


ONE_DAY = datetime.timedelta(hours=24)


class TideWindows(ListAPIView):
    """
    Get time windows where the tide prediction is above a given height.
    Valid parameters are `start` and `end` (in format `2014-05-01T00:17:00Z`)
    and `tide_level` in metres.
    """
    renderer_classes = replace_json_renderer(ListAPIView.renderer_classes)
    serializer_class = TideWindowSerializer

    def get_queryset(self, query_params=None, *args, **kwargs):
        if query_params is None:
            query_params = self.request.query_params

        location = parse_location(self.kwargs.get('location_slug', None))
        time_range = parse_time_range(
            query_params.get('start', None),
            query_params.get('end', None)
        )

        min_tide_level = parse_tide_level(
            self.request.query_params.get('tide_level'))

        extended_time_range = TimeRange(
            start=time_range.start - ONE_DAY,
            end=time_range.end + ONE_DAY)

        predictions = get_queryset(location, extended_time_range).filter(
            tide_level__gte=min_tide_level)

        tide_windows = split_predictions_into_tide_windows(predictions)
        return filter(None, map(
            partial(transform_time_window, time_range, extended_time_range),
            tide_windows))


def transform_time_window(time_range, extended_time_range, window):
    if not window.is_inside_time_range(time_range):
        return None

    if window.extends_after(extended_time_range.end):
        window.truncate_end(time_range.end)

    if window.extends_before(extended_time_range.start):
        window.truncate_start(time_range.start)

    if window.validate():
        return window
