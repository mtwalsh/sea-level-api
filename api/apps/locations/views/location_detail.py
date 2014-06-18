from rest_framework import generics

from ..serializers import LocationSerializer
from ..models import Location


class LocationDetail(generics.RetrieveAPIView):
    model = Location
    serializer_class = LocationSerializer
    lookup_field = 'slug'
