import datetime
from itertools import tee

try:
    from itertools import izip as zip  # on Python 2 replace zip with izip
except ImportError:
    pass  # Python 3 has zip already


from django.db.models import Max
from django.core.management.base import BaseCommand

from api.apps.ea_sea_levels.models import Measurement, Station
from api.apps.observations.utils import create_observation


class Command(BaseCommand):
    """
    Convert EA measurements into 1-minute observations which are relative to
    Admiralty Chart Datum.
    """
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for station in Station.objects.all():
            update_observations(station, self.stdout)


def update_observations(station, stdout):
    if observations_up_to_date(station):
        stdout.write("Nothing to do for {}".format(station))
        return

    stdout.write("Converting measurements at {} => {}".format(
        station, station.location))

    start = get_latest_observation(station.location)
    end = get_latest_ea_measurement(station)

    for dt, value, is_interp in make_linear_interpolations(start, end):
        new_value = convert_to_chart_datum(station, value)
        create_observation(station.location, dt, new_value, is_interp)


def observations_up_to_date(ea_station):
    latest_ea_measurement = get_latest_ea_measurement(ea_station)

    if latest_ea_measurement is None:
        return True

    print("Latest EA measurement: {}".format(latest_ea_measurement))

    latest_observation = get_latest_observation(ea_station.location)
    if latest_observation is None:
        return False

    print("Latest observation: {}".format(latest_observation))

    return latest_observation >= latest_ea_measurement


def get_latest_ea_measurement(ea_station):
    max_datetime = ea_station.measurements.all().aggregate(Max('datetime'))

    return max_datetime.get('datetime__max', None)


def get_latest_observation(location):
    max_datetime = location.observations.all().aggregate(
        Max('minute__datetime'))
    return max_datetime.get('minute__datetime__max', None)


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def dedupe_adjacent(original_function):
    def new_function(*args, **kwargs):
        last = None
        for value in original_function(*args, **kwargs):
            if value != last:
                yield value
            last = value
    return new_function


@dedupe_adjacent
def make_linear_interpolations(start, end):
    measurements = get_measurements(start, end)

    for measure_1, measure_2 in pairwise(measurements):
        mins_between = to_minutes(measure_2.datetime - measure_1.datetime)
        if mins_between > 15:
            continue

        delta_y = ((measure_2.measurement - measure_1.measurement)
                   / mins_between)

        yield (measure_1.datetime, rounded(measure_1.measurement), False)
        for i in range(1, mins_between):
            dt = measure_1.datetime + datetime.timedelta(minutes=i)
            yield (dt, rounded(measure_1.measurement + delta_y * i), True)
        yield (measure_2.datetime, rounded(measure_2.measurement), False)


def get_measurements(start, end):
    measurements = Measurement.objects.all()
    if start is not None:
        measurements = measurements.filter(datetime__gte=start)
    if end is not None:
        measurements = measurements.filter(datetime__lte=end)
    return measurements


def rounded(x):
    return round(x, 2)


def to_minutes(timedelta):
    mins = timedelta.total_seconds() / 60
    assert int(mins) == mins
    return int(mins)


def convert_to_chart_datum(station, value):
    return value + station.chart_datum_offset
