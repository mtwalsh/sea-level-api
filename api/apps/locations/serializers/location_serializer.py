from rest_framework import serializers

from ..models import Location


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location
        fields = ('name', 'slug', 'url')
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        resource_name = 'locations'
