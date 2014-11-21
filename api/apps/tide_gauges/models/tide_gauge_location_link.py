from django.db import models

from django.utils.encoding import python_2_unicode_compatible

from api.apps.locations.models import Location
from .tide_gauge import TideGauge


@python_2_unicode_compatible
class TideGaugeLocationLink(models.Model):
    """
    Specifies which TideGauge feeds into a Location. RawMeasurements from this
    TideGauge will be processed and copied as Observations for the Location.
    """
    class Meta:
        app_label = 'tide_gauges'

    tide_gauge = models.OneToOneField(TideGauge)
    location = models.OneToOneField(Location)

    comment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '{} => {}'.format(self.tide_gauge, self.location)
