from rest_framework.generics import ListAPIView

from api.libs.json_envelope_renderer import replace_json_renderer

from ..models import Prediction
from ..serializers import TideLevelSerializer

from .helpers import get_prediction_queryset


class TideLevels(ListAPIView):
    """
    Get tidal predictions at a given location. Valid parameters are
    `start` and `end` (in format `2014-05-01T00:17:00Z`)
    """
    renderer_classes = replace_json_renderer(ListAPIView.renderer_classes)
    serializer_class = TideLevelSerializer

    def get_queryset(self):
        return get_prediction_queryset(
            self.kwargs.get('location_slug', None),
            self.request.QUERY_PARAMS.get('start', None),
            self.request.QUERY_PARAMS.get('end', None)
        )[:60]  # limit to 60
