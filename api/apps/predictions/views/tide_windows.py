from collections import namedtuple

from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView

from api.libs.json_envelope_renderer import replace_json_renderer

from ..serializers import TideWindowSerializer

from .helpers import get_prediction_queryset, split_prediction_windows


TimeWindow = namedtuple('TimeWindow', 'first_prediction,last_prediction')


class MissingParameterException(APIException):
    status_code = 400
    default_detail = 'Missing query parameter in URL.'


class TideWindows(ListAPIView):
    """
    Get time windows where the tide prediction is above a given height.
    Valid parameters are `start` and `end` (in format `2014-05-01T00:17:00Z`)
    and `tide_level` in metres.
    """
    renderer_classes = replace_json_renderer(ListAPIView.renderer_classes)
    serializer_class = TideWindowSerializer

    def get_queryset(self, *args, **kwargs):

        try:
            min_tide_level = float(self.request.QUERY_PARAMS['tide_level'])
        except KeyError:
            raise MissingParameterException(
                'Missing required query parameter `tide_level`')

        predictions = get_prediction_queryset(
            self.kwargs['location_slug'],
            self.request.QUERY_PARAMS.get('start', None),
            self.request.QUERY_PARAMS.get('end', None)
        ).filter(tide_level__gte=min_tide_level)

        return list(make_tide_time_windows(predictions))


def make_tide_time_windows(all_predictions_above_threshold):
    for start, end in split_prediction_windows(
            all_predictions_above_threshold):
        yield TimeWindow(
            first_prediction=start,
            last_prediction=end
        )
