from rest_framework import serializers

from ..views.helpers import DATETIME_FORMAT


class TideWindowSerializer(serializers.Serializer):
    start = serializers.SerializerMethodField('get_start')
    end = serializers.SerializerMethodField('get_end')
    duration = serializers.SerializerMethodField('get_duration')

    class Meta:
        resource_name = 'tide_windows'

    @staticmethod
    def _serialize_prediction(prediction):
        return {
            'datetime': prediction.datetime.strftime(DATETIME_FORMAT),
            'tide_level': prediction.tide_level
        }

    def get_start(self, obj):
        return self._serialize_prediction(obj.start_prediction)

    def get_end(self, obj):
        return self._serialize_prediction(obj.end_prediction)

    def get_duration(self, obj):
        """
        Predictions are minutely, and the time window is defined by the first
        and last minute where the level is above a certain amount. That means
        the duration is *inclusive* of the final time - so we add a minute.
        """
        timediff = obj.end_prediction.datetime - obj.start_prediction.datetime
        return {'total_seconds': timediff.total_seconds() + 60}
