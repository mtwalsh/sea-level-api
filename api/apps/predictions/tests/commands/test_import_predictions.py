from __future__ import unicode_literals

import datetime
import pytz

from django.test import TestCase

from nose.tools import assert_equal

from api.apps.locations.models import Location
from api.apps.predictions.models import TidePrediction
from api.apps.predictions.utils import create_tide_prediction

from api.apps.predictions.management.commands.import_predictions import (
    do_load_predictions, delete_existing_predictions)

try:
    from io import StringIO         # Python 3
except ImportError:
    from cStringIO import StringIO  # Python 2


class TestImportTidePredictionsCommand(TestCase):
    fixtures = ['api/apps/locations/fixtures/two_locations.json']

    TEST_CSV = ('datetime,predicted_tide_level\n'
                '2014-06-01T00:00:00Z,8.55\n'
                '2014-06-01T00:01:00Z,8.56\n')

    @classmethod
    def setUp(cls):
        cls.csv_fobj = StringIO(cls.TEST_CSV)
        cls.liverpool = Location.objects.get(slug='liverpool')

    @staticmethod
    def _serialize(prediction):
        return {
            'location': prediction.location.slug,
            'minute__datetime': prediction.minute.datetime,
            'tide_level': prediction.tide_level
        }

    def test_load_predictions(self):
        do_load_predictions(self.liverpool, self.csv_fobj)
        assert_equal([
            {
                'minute__datetime': datetime.datetime(2014, 6, 1, 0, 0,
                                                      tzinfo=pytz.UTC),
                'location': 'liverpool',
                'tide_level': 8.55
            },
            {
                'minute__datetime': datetime.datetime(2014, 6, 1, 0, 1,
                                                      tzinfo=pytz.UTC),
                'location': 'liverpool',
                'tide_level': 8.56
            }
        ],
            [self._serialize(p) for p in TidePrediction.objects.all()]
        )

    def test_load_predictions_can_update_existing_prediction(self):
        dt = datetime.datetime(2014, 6, 1, 0, 0, tzinfo=pytz.UTC)
        create_tide_prediction(self.liverpool, dt, 8.0)
        do_load_predictions(self.liverpool, self.csv_fobj)
        assert_equal(
            {
                'minute__datetime': datetime.datetime(2014, 6, 1, 0, 0,
                                                      tzinfo=pytz.UTC),
                'location': 'liverpool',
                'tide_level': 8.55
            },
            self._serialize(TidePrediction.objects.get(minute__datetime=dt)))


class TestDeleteExistingTidePredictions(TestCase):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
    ]

    @classmethod
    def setUp(cls):
        cls.liv = Location.objects.get(slug='liverpool')
        cls.south = Location.objects.get(slug='southampton')
        cls.datetime = datetime.datetime(
            2014, 8, 3, 13, 0, tzinfo=pytz.UTC)

        for location in (cls.liv, cls.south):
            for minute in range(10):
                dt = cls.datetime + datetime.timedelta(minutes=minute)
                create_tide_prediction(location, dt, 10.0)

    def test_that_only_the_given_location_is_deleted(self):
        delete_existing_predictions(
            self.liv,
            self.datetime - datetime.timedelta(hours=1),
            self.datetime + datetime.timedelta(hours=1))

        assert_equal(
            0,
            len(TidePrediction.objects.filter(location=self.liv)))
        assert_equal(
            10,
            len(TidePrediction.objects.filter(location=self.south)))

    def test_that_predictions_arent_deleted_before_start_datetime(self):
        distant_future = self.datetime + datetime.timedelta(hours=1)
        delete_existing_predictions(
            self.liv,
            self.datetime + datetime.timedelta(minutes=3),  # 4th: 13:03
            distant_future)

        remaining_predictions = TidePrediction.objects.filter(
            location=self.liv)
        assert_equal(3, remaining_predictions.count())
        assert_equal(
            self.datetime + datetime.timedelta(minutes=2),
            list(remaining_predictions)[-1].minute.datetime)

    def test_that_predictions_arent_deleted_before_end_datetime(self):
        distant_past = self.datetime - datetime.timedelta(hours=1)
        delete_existing_predictions(
            self.liv,
            distant_past,
            self.datetime + datetime.timedelta(minutes=4))

        remaining_predictions = TidePrediction.objects.filter(
            location=self.liv)
        assert_equal(5, remaining_predictions.count())
        assert_equal(
            self.datetime + datetime.timedelta(minutes=5),
            remaining_predictions[0].minute.datetime)
