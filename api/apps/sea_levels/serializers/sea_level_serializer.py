from rest_framework import serializers

from ..models import CombinedPredictionObservation


class SeaLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CombinedPredictionObservation
        resource_name = 'sea_levels'
        fields = ('datetime', 'predicted_tide_level', 'predicted_is_high',
                  'predicted_surge_level', 'predicted_sea_level',
                  'observed_sea_level', 'derived_surge_level')
