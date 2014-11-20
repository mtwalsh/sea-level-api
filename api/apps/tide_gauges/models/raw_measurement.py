from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .tide_gauge import TideGauge
from api.apps.observations.utils import create_observation


@python_2_unicode_compatible
class RawMeasurement(models.Model):
    class Meta:
        app_label = 'tide_gauges'
        ordering = ['datetime']
        unique_together = ('tide_gauge', 'datetime')

    tide_gauge = models.ForeignKey(TideGauge, related_name='raw_measurements')
    datetime = models.DateTimeField(
        help_text='The date & time (according to the tide gauge) for which '
                  'the measurement is valid.')
    height = models.FloatField(
        help_text='The tide gauge measurement in metres.')

    def save(self, *args, **kwargs):
        linked_location = self.tide_gauge.linked_location
        if linked_location is not None:
            create_observation(
                linked_location, self.datetime, self.height, False)

        super(RawMeasurement, self).save(*args, **kwargs)

    def __str__(self):
        return '{}m'.format(self.height)
