import datetime
import pytz

from django.test import TestCase

from nose.tools import assert_equal

from api.apps.locations.models import Location
from api.apps.predictions.models import Prediction

from api.apps.predictions.management.commands.import_predictions import (
    load_predictions, nuke_predictions)

from cStringIO import StringIO


class TestImportPredictionsCommand(TestCase):
    fixtures = ['api/apps/locations/fixtures/two_locations.json']

    TEST_CSV = ('datetime,predicted_height\n'
                '2014-06-01T00:00:00+00:00,8.55\n'
                '2014-06-01T00:01:00+00:00,8.56\n')

    @classmethod
    def setUp(cls):
        cls.csv_fobj = StringIO(cls.TEST_CSV)
        cls.liverpool = Location.objects.get(slug='liverpool')

    @staticmethod
    def _serialize(prediction):
        return {
            'location': prediction.location.slug,
            'datetime': prediction.datetime,
            'tide_level': prediction.tide_level
        }

    def test_load_predictions(self):
        load_predictions(self.csv_fobj, self.liverpool)
        assert_equal([
            {
                'datetime': datetime.datetime(2014, 6, 1, 0, 0,
                                              tzinfo=pytz.UTC),
                'location': u'liverpool',
                'tide_level': 8.55
            },
            {
                'datetime': datetime.datetime(2014, 6, 1, 0, 1,
                                              tzinfo=pytz.UTC),
                'location': u'liverpool',
                'tide_level': 8.56
            }
        ],
            [self._serialize(p) for p in Prediction.objects.all()]
        )


class TestNukePredictions(TestCase):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
        'api/apps/predictions/fixtures/predictions_two_locations.json',
    ]

    @classmethod
    def setUp(cls):
        cls.liv = Location.objects.get(slug='liverpool')
        cls.south = Location.objects.get(slug='southampton')

    def test_that_nuke_only_nukes_the_given_location(self):
        assert_equal(3, len(Prediction.objects.filter(location=self.liv)))
        assert_equal(3, len(Prediction.objects.filter(location=self.south)))

        nuke_predictions(self.liv)

        assert_equal(0, len(Prediction.objects.filter(location=self.liv)))
        assert_equal(3, len(Prediction.objects.filter(location=self.south)))
