from django.core.management.base import BaseCommand

from api.apps.ea_sea_levels.models import Station, Measurement

from api.libs.ea_measurement_collector import download_recent_measurements


class Command(BaseCommand):
    docs = "Usage: get_latest_ea_measurements"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for station in Station.objects.all():
            self.stdout.write("Getting measurement(s) for {}".format(station))
            for result in download_recent_measurements(station.station_id):
                validate_datum(result.datum, station.site_datum)
                validate_station(result.station_id, station.station_id)
                self.record_measurement(station, result)

    def record_measurement(self, station, result):
        self.stdout.write("parse result: {}".format(result))
        obj, created = Measurement.objects.update_or_create(
            station=station,
            datetime=result.datetime,
            defaults={'measurement': result.measurement})
        if created:
            self.stdout.write("Saved new measurement.")
        else:
            self.stdout.write("Updated measurement.")


def validate_datum(reported_datum, site_datum):
    assert reported_datum == site_datum


def validate_station(reported_station_id, station_id):
    assert reported_station_id == station_id
