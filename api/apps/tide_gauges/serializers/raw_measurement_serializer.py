import logging
logger = logging.getLogger(__name__)

from rest_framework import serializers
from ..models import RawMeasurement


class RawMeasurementSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    height = serializers.FloatField()

    class Meta:
        model = RawMeasurement

    def update(self, instance, validated_data):
        # responsible for updating AND saving instance based on validated_data
        logging.info('RawMeasurementSerializer.update({}, {})'.format(
            instance, validated_data))

        assert instance.datetime == validated_data['datetime']
        assert instance.tide_gauge == validated_data['tide_gauge']

        if instance.height != validated_data['height']:
            instance.height = validated_data['height']
            instance.save()

        return instance

    def create(self, validated_data):
        logging.info('RawMeasurementSerializer.create({})'.format(
            validated_data))
        instance = RawMeasurement.objects.create(**validated_data)
        logging.info(instance)
        return instance


class RawMeasurementListSerializer(serializers.ListSerializer):
    child = RawMeasurementSerializer()

    def save(self, tide_gauge):
        # Adapted from save() in parent ListSerializer

        validated_data = [
            dict(list(attrs.items()) + [('tide_gauge', tide_gauge)])
            for attrs in self.validated_data
        ]

        def create_or_update(attrs):
            try:
                existing = tide_gauge.raw_measurements.get(
                    datetime=attrs['datetime'])
            except RawMeasurement.DoesNotExist:
                return self.child.create(attrs)
            else:
                return self.child.update(existing, attrs)

        self.instance = [
            create_or_update(attrs) for attrs in validated_data
        ]

        return self.instance
