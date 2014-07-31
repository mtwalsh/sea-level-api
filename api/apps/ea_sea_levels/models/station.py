from django.db import models

from api.apps.locations.models import Location

from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Station(models.Model):
    class Meta:
        app_label = 'ea_sea_levels'

    location = models.ForeignKey(
        Location,
        help_text='The location to which this measurement station relates')

    station_name = models.CharField(
        max_length=50,
        help_text='The EA name given to the station.')

    station_id = models.IntegerField(
        help_text='The EA numeric ID assigned to the station.')

    site_datum = models.CharField(
        max_length=10,
        help_text='The datum against which a measurement is taken.')

    def __str__(self):
        return self.station_name
