from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from api.apps.locations.models import Location
from api.libs.minute_in_time.models import Minute


@python_2_unicode_compatible
class SurgePrediction(models.Model):
    class Meta:
        app_label = 'predictions'
        unique_together = ('location', 'minute')

    minute = models.ForeignKey(
        Minute,
        related_name='surge_predictions'
    )

    location = models.ForeignKey(Location)

    surge_level = models.FloatField(
        help_text='The predicted additional height on top of the tide '
                  'prediction due to other conditions such as weather.')

    def __str__(self):
        return "{}".format(self.surge_level)
