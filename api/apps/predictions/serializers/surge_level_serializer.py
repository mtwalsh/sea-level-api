import pytz

from rest_framework import serializers

from ..models import SurgePrediction
from ..utils import create_surge_prediction

import logging
logger = logging.getLogger(__name__)


class SurgeLevelSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    surge_level = serializers.FloatField()

    class Meta:
        model = SurgePrediction

    def update(self, instance, validated_data):
        # responsible for updating AND saving instance based on validated_data
        logging.info('SurgeLevelSerializer.update({}, {})'.format(
            instance, validated_data))

        assert instance.minute.datetime == validated_data['datetime']
        assert instance.location == validated_data['location']

        if instance.surge_level != validated_data['surge_level']:
            instance.surge_level = validated_data['surge_level']
            instance.save()

        return instance

    def create(self, validated_data):
        logging.info('SurgeLevelSerializer.create({})'.format(validated_data))
        instance = create_surge_prediction(**validated_data)
        logging.info(instance)
        return instance

    def validate_datetime(self, dt):
        try:
            if dt.tzinfo != pytz.UTC:
                raise serializers.ValidationError(
                    'datetime must be UTC eg `2014-06-10 10:34:00Z`')
        except AttributeError:
            raise serializers.ValidationError(
                'error accessing datetime.tzinfo on {} with type {}'.format(
                    dt, type(dt)))

        return dt
