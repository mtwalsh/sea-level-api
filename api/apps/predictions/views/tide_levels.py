from rest_framework.generics import ListAPIView

from api.libs.json_envelope_renderer import replace_json_renderer
from api.libs.param_parsers import parse_interval

from ..serializers import TideLevelSerializer

from .helpers import parse_and_get_queryset


class TideLevels(ListAPIView):
    """
    Get tidal predictions at a given location. Valid parameters are
    `start` and `end` (in format `2014-05-01T00:17:00Z`) and `interval` in
    minutes.
    """
    renderer_classes = replace_json_renderer(ListAPIView.renderer_classes)
    serializer_class = TideLevelSerializer

    def get_queryset(self, query_params=None, *args, **kwargs):
        if query_params is None:
            query_params = self.request.QUERY_PARAMS

        interval_mins = parse_interval(query_params.get('interval', '1'))

        return parse_and_get_queryset(
            self.kwargs.get('location_slug', None),
            query_params.get('start', None),
            query_params.get('end', None)
        )[:24 * 60:interval_mins]  # limit to 24 hours of data
