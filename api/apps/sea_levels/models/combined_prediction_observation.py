from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from api.apps.locations.models import Location


@python_2_unicode_compatible
class CombinedPredictionObservation(models.Model):
    class Meta:
        app_label = 'sea_levels'
        managed = False

    datetime = models.DateTimeField(primary_key=True)
    location = models.ForeignKey(
        Location,
        null=False,
        on_delete=models.DO_NOTHING)
    predicted_tide_level = models.FloatField(null=False)
    predicted_surge_level = models.FloatField(null=False)
    predicted_sea_level = models.FloatField(null=False)
    observed_sea_level = models.FloatField(null=True)
    derived_surge_level = models.FloatField(null=True)

    def __str__(self):
        return "{}".format(self.datetime)
