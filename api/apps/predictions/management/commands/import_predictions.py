import csv
import datetime

import pytz

from batcher import batcher

from django_docopt_command import DocOptCommand
from api.apps.predictions.models import Prediction
from api.apps.locations.models import Location


class Command(DocOptCommand):
    docs = "Usage: import_predictions [--nuke-first] <location> <filename>"

    def handle_docopt(self, arguments):
        self.stdout.write(str(arguments))
        location = Location.objects.get(slug=arguments['<location>'])

        with open(arguments['<filename>'], 'r') as f:
            if arguments['--nuke-first'] is True:
                nuke_predictions(location)

            load_predictions(f, location, self.stdout)


def nuke_predictions(location_obj):
    Prediction.objects.filter(location=location_obj).delete()


def load_predictions(f, location_obj, stdout=None):
    count = 0
    with batcher(Prediction.objects.bulk_create, 999) as b:
        for row in csv.DictReader(f):
            count += 1
            if stdout is not None and 0 == (count % 1000):
                stdout.write(str(count))

            b.push(Prediction(
                location=location_obj,
                datetime=parse_datetime(row['datetime']),
                tide_level=float(row['predicted_height'])))


def parse_datetime(datetime_str):
    return datetime.datetime.strptime(
        datetime_str, '%Y-%m-%dT%H:%M:%S+00:00').replace(
        tzinfo=pytz.UTC)
