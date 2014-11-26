from rest_framework import serializers

from ..models import TidePrediction


class TideLevelSerializer(serializers.ModelSerializer):
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = TidePrediction
        resource_name = 'tide_levels'
        fields = ('tide_level', 'datetime', 'is_high_tide')

    def get_datetime(self, obj):
        return obj.minute.datetime
