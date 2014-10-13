from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from api.apps.locations.models import Location


@python_2_unicode_compatible
class LocationStatusConfig(models.Model):
    class Meta:
        app_label = 'status'

    location = models.OneToOneField(Location, related_name='status_config')
    tide_predictions_alerts_disabled_until = models.DateTimeField(
        null=True, blank=True,
        help_text='After this date/time, turn on alerts for tide '
                  'predictions at this location. Set to blank to turn on '
                  'immediately.')

    surge_predictions_alerts_disabled_until = models.DateTimeField(
        null=True, blank=True,
        help_text='After this date/time, turn on alerts for surge '
                  'predictions at this location. Set to blank to turn on '
                  'immediately.')

    observations_alerts_disabled_until = models.DateTimeField(
        null=True, blank=True,
        help_text='After this date/time, turn on alerts for observations '
                  'at this location. Set to blank to turn on immediately.')

    def disabled_alerts(self):
        from ..alert_manager import alerts_disabled
        disabled = [a.name for a in alerts_disabled(self.location)]
        return ', '.join(sorted(disabled)) if disabled else ''

    def __str__(self):
        return "{}".format(self.location)
