from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from api.apps.locations.models import Location
from api.libs.minute_in_time.models import Minute


@python_2_unicode_compatible
class TidePrediction(models.Model):
    class Meta:
        app_label = 'predictions'
        unique_together = ('location', 'minute')

    minute = models.ForeignKey(
        Minute,
        related_name='predictions'
    )

    location = models.ForeignKey(Location)

    tide_level = models.FloatField(
        help_text='The predicted height in metres of the tidal component '
                  'of the sea level above a known datum.')

    is_high_tide = models.BooleanField(
        default=False,
        help_text='Does this tide prediction correspond to a high tide.')

    def __str__(self):
        return "{}".format(self.tide_level)
