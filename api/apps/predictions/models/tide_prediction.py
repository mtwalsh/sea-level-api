from django.db import models

from api.apps.locations.models import Location


class TidePrediction(models.Model):
    class Meta:
        app_label = 'predictions'

    datetime = models.DateTimeField(unique=True)

    height = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text='The predicted height in metres of the tidal component '
                  'of the sea level.')
    location = models.ForeignKey(Location)
