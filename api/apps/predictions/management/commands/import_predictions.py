import csv
import datetime

import pytz

from batcher import batcher

from django.conf import settings

from django_docopt_command import DocOptCommand
from api.apps.predictions.models import TidePrediction
from api.apps.locations.models import Location
from api.libs.minute_in_time.models import Minute


class Command(DocOptCommand):
    docs = "Usage: import_predictions <location> <filename>"

    def handle_docopt(self, arguments):
        location = Location.objects.get(slug=arguments['<location>'])

        with open(arguments['<filename>'], 'r') as f:
            do_load_predictions(location, f)


def do_load_predictions(location, f):

    datetimes_in_csv = get_datetimes(f)
    start = min(datetimes_in_csv)
    end = max(datetimes_in_csv)

    missing_datetimes = (
        datetimes_in_csv - set(get_existing_datetimes(start, end)))

    bulk_create_minutes(missing_datetimes)
    del missing_datetimes

    minutes_hash = make_minutes_hash(start, end)
    delete_existing_predictions(location, start, end)
    f.seek(0)
    create_predictions(f, location, minutes_hash)


def get_datetimes(f):
    print("Getting all datetimes from CSV")
    reader = csv.DictReader(f)
    return set(parse_datetime(row['datetime']) for row in reader)


def get_existing_datetimes(start, end):
    print("Finding existing Minutes between {} and {}".format(start, end))
    return (m.datetime for m in get_existing_minutes(start, end))


def get_existing_minutes(start, end):
    return Minute.objects.filter(
        datetime__gte=start,
        datetime__lte=end)


def bulk_create_minutes(datetimes):
    print("Creating missing Minute objects")
    Minute.objects.bulk_create(Minute(datetime=dt) for dt in datetimes)


def delete_existing_predictions(location_obj, start, end):
    print("Deleting predictions for {} from {} to {}".format(
        location_obj, start, end))
    assert isinstance(start, datetime.datetime), start
    assert isinstance(end, datetime.datetime), end
    TidePrediction.objects.filter(
        location=location_obj,
        minute__datetime__gte=start,
        minute__datetime__lte=end).delete()


def make_minutes_hash(start, end):
    print("Making hash datetime -> Minute")
    return {m.datetime: m for m in get_existing_minutes(start, end)}


def create_predictions(f, location_obj, minutes_hash):
    print("Creating TidePredictions")
    count = 0
    with batcher(TidePrediction.objects.bulk_create, 999) as b:
        for row in csv.DictReader(f):
            count += 1
            if 0 == (count % 1000):
                print(str(count))

            b.push(TidePrediction(
                location=location_obj,
                minute=minutes_hash[parse_datetime(row['datetime'])],
                tide_level=float(row['predicted_tide_level']),
                is_high_tide=parse_bool(row['is_high_tide'])))


def parse_datetime(datetime_str):
    return datetime.datetime.strptime(
        datetime_str, settings.DATETIME_FORMAT).replace(
        tzinfo=pytz.UTC)


def parse_bool(bool_string):
    """
    >>> parse_bool('1')
    True
    >>> parse_bool('0')
    False
    >>> parse_bool('')
    False
    """
    return '1' == bool_string
