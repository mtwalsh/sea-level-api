from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .station import Station


@python_2_unicode_compatible
class Measurement(models.Model):
    class Meta:
        app_label = 'ea_sea_levels'

    station = models.ForeignKey(Station, related_name='measurements')
    datetime = models.DateTimeField(
        help_text='The date & time at which the measurement was taken')
    measurement = models.FloatField(
        help_text='The tide level measurement in metres.')

    def __str__(self):
        return '{}m'.format(self.measurement)
