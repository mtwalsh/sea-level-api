from __future__ import print_function

import csv
import datetime
import os

from itertools import tee

import pytz

from django.conf import settings
from django_docopt_command import DocOptCommand

from api.apps.predictions.utils import create_surge_prediction
from api.apps.surge_model_converter.models import ModelLocation


class Command(DocOptCommand):
    docs = """
Usage:
  import_surge_predictions <filenames>... [--traceback] [--skip-already-loaded]

Options:
  --traceback             Raise on exception
  --skip-already-loaded   Keep track of files that have already been
                          successfully loaded and don't reload them.
    """

    def handle_docopt(self, arguments):
        filenames = arguments['<filenames>']
        for filename in filenames:
            if arguments['--skip-already-loaded'] and already_loaded(filename):
                self.stdout.write("Skipping {}".format(filename))
                continue

            self.stdout.write('Loading {}'.format(filename))

            with open(filename, 'r') as f:
                do_load_predictions(f, print_func=self.stdout.write)
                record_loaded(filename)


def already_loaded(filename):
    csv_filename = get_loading_log_csv_filename(filename)
    if not os.path.exists(csv_filename):
        return False

    (_, base_filename) = os.path.split(filename)
    with open(csv_filename, 'r') as f:
        loaded_filenames = set(row['filename'] for row in csv.DictReader(f))
        return base_filename in loaded_filenames


def record_loaded(filename):
    if already_loaded(filename):
        return

    csv_filename = get_loading_log_csv_filename(filename)
    if not os.path.exists(csv_filename):
        with open(csv_filename, 'w') as f:
            f.write('filename,datetime\n')

    with open(csv_filename, 'a') as f:
        dirname, basename = os.path.split(filename)
        f.write('{},{}\n'.format(basename, datetime.datetime.now(pytz.UTC)))


def get_loading_log_csv_filename(filename):
    dirname, basename = os.path.split(filename)
    return os.path.join(dirname, 'load_log.csv')


def do_load_predictions(f, print_func=print):
    location_hash = load_model_location_codes()
    for location_code, location_model in location_hash.items():
        print_func('Reading values for {}'.format(location_code))
        times_and_values = get_values_for_code(f, location_code)
        f.seek(0)

        for i, (dt, value) in enumerate(
                interpolate_to_minute(times_and_values)):
            if 0 == i % 200:
                print_func('{}'.format(i))
            create_surge_prediction(location_model.location, dt, value)


def get_values_for_code(csv_fobj, location_code):
    for row in csv.DictReader(csv_fobj):
        if row['location_noc_surge_model'] == location_code:
            yield (
                parse_datetime(row['datetime']),
                float(row['predicted_surge_level'])
            )


def parse_datetime(datetime_string):
    return datetime.datetime.strptime(
        datetime_string, settings.DATETIME_FORMAT).replace(tzinfo=pytz.UTC)


def load_model_location_codes():
    """
    Return a dictionary ie {'LVPL': <ModelLocation 'LVPL'>} for each
    ModelLocation in the database.
    """
    return {m.surge_model_name: m for m in ModelLocation.objects.all()}


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def interpolate_to_minute(times_and_values):
    for (t0, y0), (t1, y1) in pairwise(times_and_values):
        yield (t0, y0)
        for time, fraction in intermediate_minutes(t0, t1):
            y = y0 + fraction * (y1 - y0)
            yield (time, y)
        yield (t1, y1)


def intermediate_minutes(dt0, dt1):
    """
    For input of 10:15, 10:20, yield:
    (10:16, 0.2)
    (10:17, 0.4)
    (10:18, 0.6)
    (10:19, 0.8)
    """
    delta_minutes = int((dt1 - dt0).total_seconds() / 60)
    for minute_offset in range(1, delta_minutes):
        fraction = float(minute_offset) / delta_minutes
        yield (dt0 + datetime.timedelta(minutes=minute_offset), fraction)
