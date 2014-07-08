from collections import namedtuple

from rest_framework.generics import ListAPIView

from api.libs.json_envelope_renderer import replace_json_renderer

from ..serializers import TideWindowSerializer

from .helpers import (parse_and_get_queryset,
                      split_prediction_windows)
from .exceptions import MissingParameterException

TimeWindow = namedtuple('TimeWindow', 'start_prediction,end_prediction')


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
            query_params = self.request.QUERY_PARAMS

        predictions = parse_and_get_queryset(
            self.kwargs.get('location_slug', None),
            query_params.get('start', None),
            query_params.get('end', None)
        )

        try:
            min_tide_level = float(self.request.QUERY_PARAMS['tide_level'])
        except KeyError:
            raise MissingParameterException(
                'Missing required query parameter `tide_level`')

        predictions = predictions.filter(tide_level__gte=min_tide_level)

        return list(make_tide_time_windows(predictions))


def make_tide_time_windows(all_predictions_above_threshold):
    for start, end in split_prediction_windows(
            all_predictions_above_threshold):
        yield TimeWindow(
            start_prediction=start,
            end_prediction=end
        )
