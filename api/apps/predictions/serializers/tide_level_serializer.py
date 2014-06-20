from rest_framework import serializers

from ..models import Prediction


class TideLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        resource_name = 'tide_levels'
        fields = ('datetime', 'tide_level')
