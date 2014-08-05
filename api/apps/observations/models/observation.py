from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from api.apps.locations.models import Location
from api.libs.minute_in_time.models import Minute


@python_2_unicode_compatible
class Observation(models.Model):
    class Meta:
        app_label = 'observations'
        unique_together = ('location', 'minute')

    location = models.ForeignKey(Location, related_name='observations')
    minute = models.ForeignKey(Minute, related_name='observations')

    is_interpolated = models.BooleanField(
        default=False,
        help_text='Whether the value was interpolated from other points or '
                  'is an actual observation.')

    sea_level = models.FloatField(
        help_text='The measured sea level height.')

    def __str__(self):
        return "{}{}".format(self.sea_level,
                             '' if self.is_interpolated else '*')
