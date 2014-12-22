from rest_framework.generics import ListAPIView

from api.apps.locations.models import Location
from api.apps.locations.serializers import LocationSerializer

from api.libs.json_envelope_renderer import replace_json_renderer


class LocationList(ListAPIView):
    """
    List all locations at which there may be sea level predictions.
    """
    renderer_classes = replace_json_renderer(ListAPIView.renderer_classes)

    queryset = Location.objects.filter(visible=True)
    serializer_class = LocationSerializer
