from django.test import TestCase
from nose.tools import assert_equal, assert_in, assert_not_in
from nose.plugins.skip import SkipTest

from api.apps.predictions.models import Prediction
from api.apps.locations.models import Location

import datetime
import json

import pytz


class TestTideLevelsView(TestCase):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
        'api/apps/predictions/fixtures/predictions_two_locations.json',
    ]

    def test_that_tide_levels_url_lists_available_locations(self):
        raise SkipTest("Not yet implemented.")
        response = self.client.get('/1/predictions/tide-levels/')
        data = json.loads(response.content)
        assert_equal([], data['tide_levels'])

        expected_linked = {
            'locations': [
                '/1/predictions/tide-levels/liverpool/',
                '/1/predictions/tide-levels/southampton/',
            ]
        }
        assert_equal(expected_linked, data['linked'])

    def test_that_invalid_location_gives_a_json_404(self):
        raise SkipTest("Not yet implemented.")

    def test_that_no_start_and_end_parameter_temporary_redirects_to_now(self):
        raise SkipTest("Not yet implemented.")
        response = self.client.get('/1/predictions/tide-levels/liverpool/')
        assert_equal(302, response.status_code)

    def test_that_envelope_has_tide_levels_field(self):
        response = self.client.get('/1/predictions/tide-levels/liverpool/')
        data = json.loads(response.content)
        assert_in('tide_levels', data)

    def test_that_tide_level_records_have_correct_structure(self):
        response = self.client.get(
            '/1/predictions/tide-levels/liverpool/'
            '?start=2014-06-17T09:00:00Z'
            '&end=2014-06-17T09:05:00Z')
        data = json.loads(response.content)
        tide_levels = data['tide_levels']
        expected = {
            'datetime': '2014-06-17T09:00:00Z',
            'tide_level': 10.3
        }
        assert_equal(expected, tide_levels[0])

    def test_that_tides_are_given_for_liverpool(self):
        response = self.client.get(
            '/1/predictions/tide-levels/liverpool/'
            '?start=2014-06-17T09:00:00Z'
            '&end=2014-06-17T09:05:00Z')
        data = json.loads(response.content)
        tide_levels = data['tide_levels']
        assert_equal(
            [10.3, 10.8, 10.9],  # Liverpool values
            [t['tide_level'] for t in tide_levels]
        )

    def test_that_tides_are_given_for_southampton(self):
        response = self.client.get(
            '/1/predictions/tide-levels/southampton/'
            '?start=2014-06-17T09:00:00Z'
            '&end=2014-06-17T09:05:00Z')
        data = json.loads(response.content)
        tide_levels = data['tide_levels']
        assert_equal(
            [4.0, 4.3, 4.1],  # Southampton values
            [t['tide_level'] for t in tide_levels]
        )

    def test_that_the_start_parameter_filters_inclusively(self):
        response = self.client.get(
            '/1/predictions/tide-levels/liverpool/'
            '?start=2014-06-17T09:00:00Z')
        data = json.loads(response.content)

        assert_in(
            '2014-06-17T09:00:00Z',
            [t['datetime'] for t in data['tide_levels']]
        )

    def test_that_the_end_parameter_filters_exclusively(self):
        response = self.client.get(
            '/1/predictions/tide-levels/liverpool/'
            '?start=2014-06-17T09:00:00Z'
            '&end=2014-06-17T09:02:00Z'
        )
        data = json.loads(response.content)
        assert_not_in(
            '2014-06-17T09:02:00Z',
            [t['datetime'] for t in data['tide_levels']]
        )


class TestTideLevelsViewLimitingQueries(TestCase):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
    ]

    @classmethod
    def setUp(cls):
        cls.base_time = datetime.datetime(2014, 6, 1, 10, 30, tzinfo=pytz.UTC)
        cls.create_lots_of_tide_level_entries()

    @classmethod
    def create_lots_of_tide_level_entries(cls):
        location = Location.objects.get(slug='liverpool')
        for minute in range(2 * 60):
            Prediction.objects.create(
                location=location,
                datetime=cls.base_time + datetime.timedelta(minutes=minute),
                tide_level=5.0
            )

    def test_that_results_are_limited_to_1_hour(self):
        response = self.client.get(
            '/1/predictions/tide-levels/liverpool/'
            '?start=2014-06-01T00:00:00Z'
            '&end=2014-06-02T00:00:00Z'
        )
        data = json.loads(response.content)
        assert_equal(1 * 60, len(data['tide_levels']))


class TestTideLevelsViewOrderingResults(TestCase):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
    ]

    @classmethod
    def setUp(cls):
        cls.base_time = datetime.datetime(2014, 6, 1, 10, 30, tzinfo=pytz.UTC)
        cls.create_unordered_tide_level_entries()

    @classmethod
    def create_unordered_tide_level_entries(cls):
        location = Location.objects.get(slug='liverpool')
        for minute in [0, 4, 2, 3, 1]:
            Prediction.objects.create(
                location=location,
                datetime=cls.base_time + datetime.timedelta(minutes=minute),
                tide_level=5.0
            )

    def test_that_results_are_ordered_by_datetime(self):
        response = self.client.get(
            '/1/predictions/tide-levels/liverpool/'
            '?start=2014-06-01T00:00:00Z'
            '&end=2014-06-02T00:00:00Z'
        )
        data = json.loads(response.content)
        datetimes = [t['datetime'] for t in data['tide_levels']]
        assert_equal(
            [
                '2014-06-01T10:30:00Z',
                '2014-06-01T10:31:00Z',
                '2014-06-01T10:32:00Z',
                '2014-06-01T10:33:00Z',
                '2014-06-01T10:34:00Z'
            ],
            datetimes)
