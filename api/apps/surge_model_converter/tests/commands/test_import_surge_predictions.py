from __future__ import unicode_literals

import datetime
import pytz

try:
    from io import StringIO         # Python 3
except ImportError:
    from cStringIO import StringIO  # Python 2

from nose.tools import assert_equal

from django.test import TestCase

from api.apps.locations.models import Location
from api.apps.surge_model_converter.models import ModelLocation
from api.apps.predictions.models import SurgePrediction

from api.apps.surge_model_converter.management.commands\
    .import_surge_predictions import (do_load_predictions,
                                      get_values_for_code,
                                      interpolate_to_minute,
                                      intermediate_minutes)

TEST_CSV = ('location_noc_surge_model,datetime,predicted_surge_level\n'
            'LVPL,2014-08-26T00:00:00Z,0.2\n'
            'LVPL,2014-08-26T00:15:00Z,0.3\n'
            'STWY,2014-08-26T00:00:00Z,-0.1\n'
            'STWY,2014-08-26T00:15:00Z,-0.2\n')


class TestDoLoadPredictions(TestCase):
    @classmethod
    def setUpClass(cls):
        liverpool = Location.objects.create(slug='liverpool', name='Liv')
        stornoway = Location.objects.create(slug='stornoway', name='Storn')

        ModelLocation.objects.create(
            surge_model_name='LVPL',
            location=liverpool)
        ModelLocation.objects.create(
            surge_model_name='STWY',
            location=stornoway)

        do_load_predictions(StringIO(TEST_CSV))

    @classmethod
    def tearDownClass(cls):
        ModelLocation.objects.all().delete()
        Location.objects.all().delete()

    def test_that_16_surge_predictions_have_been_created_for_liverpool(self):
        assert_equal(16, SurgePrediction.objects.filter(
            location__slug='liverpool').count())

    def test_that_16_surge_predictions_have_been_created_for_stornoway(self):
        assert_equal(16, SurgePrediction.objects.filter(
            location__slug='stornoway').count())

    def test_that_prediction_datetimes_are_correct_for_liverpool(self):
        datetimes = [p.minute.datetime
                     for p in SurgePrediction.objects.filter(
                         location__slug='liverpool')]

        expected_datetimes = [
            datetime.datetime(2014, 8, 26, 0, i, tzinfo=pytz.UTC)
            for i in range(16)]

        assert_equal(expected_datetimes, datetimes)

    def test_that_prediction_datetimes_are_correct_for_stornoway(self):
        datetimes = [p.minute.datetime
                     for p in SurgePrediction.objects.filter(
                         location__slug='stornoway')]

        expected_datetimes = [
            datetime.datetime(2014, 8, 26, 0, i, tzinfo=pytz.UTC)
            for i in range(16)]

        assert_equal(expected_datetimes, datetimes)

    def test_that_prediction_values_are_correct_for_liverpool(self):
        values = [p.surge_level
                  for p in SurgePrediction.objects.filter(
                      location__slug='liverpool')]

        expected_values = [0.2, 0.2067, 0.2133, 0.22, 0.2267, 0.2333, 0.24,
                           0.2467, 0.2533, 0.26, 0.2667, 0.2733, 0.28, 0.2867,
                           0.2933, 0.3]
        assert_equal(expected_values, [round(x, 4) for x in values])

    def test_that_prediction_values_are_correct_for_stornoway(self):
        values = [p.surge_level
                  for p in SurgePrediction.objects.filter(
                      location__slug='stornoway')]

        expected_values = [-0.1, -0.1067, -0.1133, -0.12, -0.1267, -0.1333,
                           -0.14, -0.1467, -0.1533, -0.16, -0.1667, -0.1733,
                           -0.18, -0.1867, -0.1933, -0.2]
        assert_equal(expected_values, [round(x, 4) for x in values])


class TestGetValuesForCode(TestCase):
    def test_that_it_retrieves_liverpool_values_correctly(self):
        expected = [
            (datetime.datetime(2014, 8, 26, 0, 0, tzinfo=pytz.UTC), 0.2),
            (datetime.datetime(2014, 8, 26, 0, 15, tzinfo=pytz.UTC), 0.3)
        ]
        result = list(get_values_for_code(StringIO(TEST_CSV), 'LVPL'))
        assert_equal(expected, result)

    def test_that_it_retrieves_stornoway_values_correctly(self):
        expected = [
            (datetime.datetime(2014, 8, 26, 0, 0, tzinfo=pytz.UTC), -0.1),
            (datetime.datetime(2014, 8, 26, 0, 15, tzinfo=pytz.UTC), -0.2)
        ]
        result = list(get_values_for_code(StringIO(TEST_CSV), 'STWY'))
        assert_equal(expected, result)


class TestInterpolateToMinute(TestCase):
    def test_an_interpolation(self):
        result = interpolate_to_minute([
            (datetime.datetime(2014, 8, 26, 0, 0, tzinfo=pytz.UTC), 1.0),
            (datetime.datetime(2014, 8, 26, 0, 5, tzinfo=pytz.UTC), 2.0),
        ])
        expected = [
            (datetime.datetime(2014, 8, 26, 0, 0, tzinfo=pytz.UTC), 1.0),
            (datetime.datetime(2014, 8, 26, 0, 1, tzinfo=pytz.UTC), 1.2),
            (datetime.datetime(2014, 8, 26, 0, 2, tzinfo=pytz.UTC), 1.4),
            (datetime.datetime(2014, 8, 26, 0, 3, tzinfo=pytz.UTC), 1.6),
            (datetime.datetime(2014, 8, 26, 0, 4, tzinfo=pytz.UTC), 1.8),
            (datetime.datetime(2014, 8, 26, 0, 5, tzinfo=pytz.UTC), 2.0),
        ]
        assert_equal(expected, list(result))


class TestIntermediateMinutes(TestCase):
    @classmethod
    def setUpClass(cls):
        dt_1 = datetime.datetime(2014, 8, 1, 10, 15, tzinfo=pytz.UTC)
        dt_2 = datetime.datetime(2014, 8, 1, 10, 20, tzinfo=pytz.UTC)
        minutes_and_fractions = intermediate_minutes(dt_1, dt_2)
        cls.minutes, cls.fractions = zip(*minutes_and_fractions)

    def test_that_the_minutes_yielded_are_correct(self):
        assert_equal((
            datetime.datetime(2014, 8, 1, 10, 16, tzinfo=pytz.UTC),
            datetime.datetime(2014, 8, 1, 10, 17, tzinfo=pytz.UTC),
            datetime.datetime(2014, 8, 1, 10, 18, tzinfo=pytz.UTC),
            datetime.datetime(2014, 8, 1, 10, 19, tzinfo=pytz.UTC)),
            self.minutes)

    def test_that_the_fractions_yielded_are_correct(self):
        assert_equal(
            (0.2, 0.4, 0.6, 0.8),
            self.fractions)
