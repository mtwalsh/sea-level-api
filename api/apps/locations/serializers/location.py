from rest_framework import serializers

from ..models import Location


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location
        lookup_field = 'slug'
        fields = ('name', 'url')
        resource_name = 'locations'
