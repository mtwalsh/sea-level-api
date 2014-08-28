from django.test import TestCase
from nose.tools import assert_equal, assert_in, assert_not_in

from api.apps.predictions.utils import create_tide_prediction
from api.apps.observations.utils import create_observation
from api.apps.locations.models import Location
from api.libs.test_utils import decode_json

import datetime

import pytz


class TestSeaLevelsViewBase(TestCase):
    BASE_PATH = '/1/sea-levels/'
    EXAMPLE_FULL_PATH = (
        BASE_PATH + 'liverpool/'
        '?start=2014-06-17T09:00:00Z'
        '&end=2014-06-17T09:05:00Z')

    fixtures = ['api/apps/locations/fixtures/two_locations.json']

    def _get(self, start, end, location='liverpool'):
        response = self.client.get(
            self.BASE_PATH + '{}/?start={}&end={}'.format(location, start, end)
        )
        return decode_json(response.content)['sea_levels']


class TestSeaLevelsView(TestSeaLevelsViewBase):
    fixtures = TestSeaLevelsViewBase.fixtures + [
        'api/apps/predictions/fixtures/predictions_two_locations.json',
    ]

    def test_that_envelope_has_sea_levels_field(self):
        response = self.client.get(self.EXAMPLE_FULL_PATH)
        data = decode_json(response.content)
        assert_in('sea_levels', data)

    def test_that_tide_level_records_have_correct_structure(self):
        response = self.client.get(self.EXAMPLE_FULL_PATH)
        data = decode_json(response.content)
        sea_levels = data['sea_levels']
        expected = {
            'datetime': '2014-06-17T09:00:00Z',
            'predicted_tide_level': 10.3,
            'observed_sea_level': None,
            'derived_surge_level': None,
        }
        assert_equal(expected, sea_levels[0])

    def test_that_tides_are_given_for_liverpool(self):
        sea_levels = self._get('2014-06-17T09:00:00Z', '2014-06-17T09:05:00Z')
        assert_equal(
            [10.3, 10.8, 10.9],  # Liverpool values
            [t['predicted_tide_level'] for t in sea_levels]
        )

    def test_that_tides_are_given_for_southampton(self):
        sea_levels = self._get('2014-06-17T09:00:00Z', '2014-06-17T09:05:00Z',
                               'southampton')
        assert_equal(
            [4.0, 4.3, 4.1],  # Southampton values
            [t['predicted_tide_level'] for t in sea_levels]
        )

    def test_that_the_start_parameter_filters_inclusively(self):
        sea_levels = self._get('2014-06-17T09:00:00Z', '2014-06-18T09:00:00Z')
        assert_in(
            '2014-06-17T09:00:00Z',
            [t['datetime'] for t in sea_levels]
        )

    def test_that_the_end_parameter_filters_exclusively(self):
        sea_levels = self._get('2014-06-17T09:00:00Z', '2014-06-17T09:02:00Z')
        assert_not_in(
            '2014-06-17T09:02:00Z',
            [t['datetime'] for t in sea_levels]
        )


class TestSeaLevelsViewShowsObservations(TestSeaLevelsViewBase):

    @classmethod
    def setUp(cls):
        base_time = datetime.datetime(2014, 6, 1, 10, 30, tzinfo=pytz.UTC)
        location = Location.objects.get(slug='liverpool')
        for minute, tide_level in [(0, 5.0), (1, 5.1), (2, 5.2)]:
            create_tide_prediction(
                location,
                base_time + datetime.timedelta(minutes=minute),
                tide_level
            )

        create_observation(
            location,
            base_time + datetime.timedelta(minutes=1),
            4.8, True)

    def test_that_observed_sea_level_is_null_when_not_present(self):
        sea_levels = self._get('2014-06-01T10:30:00Z', '2014-06-17T10:31:00Z')
        assert_equal(
            None,
            sea_levels[0]['observed_sea_level'])

    def test_that_derived_surge_level_is_null_when_not_present(self):
        sea_levels = self._get('2014-06-01T10:30:00Z', '2014-06-17T10:31:00Z')
        assert_equal(
            None,
            sea_levels[0]['derived_surge_level'])

    def test_that_observed_sea_level_is_correct_when_present(self):
        sea_levels = self._get('2014-06-01T10:31:00Z', '2014-06-17T10:32:00Z')
        assert_equal(
            4.8,
            sea_levels[0]['observed_sea_level'])

    def test_that_derived_surge_level_is_calculated_correctly(self):
        sea_levels = self._get('2014-06-01T10:31:00Z', '2014-06-17T10:32:00Z')
        assert_equal(
            -0.3,  # tide=5.1, observation=4.8
            sea_levels[0]['derived_surge_level'])


class TestSeaLevelsViewLimitingQueries(TestSeaLevelsViewBase):
    @classmethod
    def setUp(cls):
        cls.base_time = datetime.datetime(2014, 6, 1, 10, 30, tzinfo=pytz.UTC)
        cls.create_lots_of_tide_level_entries()

    @classmethod
    def create_lots_of_tide_level_entries(cls):
        location = Location.objects.get(slug='liverpool')
        for minute in range(30 * 60):
            create_tide_prediction(
                location,
                cls.base_time + datetime.timedelta(minutes=minute),
                5.0
            )

    def test_that_results_are_limited_to_24_hours_1440_records(self):
        response = self.client.get(
            self.BASE_PATH + 'liverpool/'
            '?start=2014-06-01T00:00:00Z'
            '&end=2014-06-03T00:00:00Z'
        )
        data = decode_json(response.content)
        assert_equal(24 * 60, len(data['sea_levels']))


class TestSeaLevelsIntevalParameter(TestSeaLevelsViewBase):
    @classmethod
    def setUp(cls):
        cls.base_time = datetime.datetime(2014, 6, 1, 10, 30, tzinfo=pytz.UTC)
        cls.create_60_entries()

    @classmethod
    def create_60_entries(cls):
        location = Location.objects.get(slug='liverpool')
        for minute in range(60):
            create_tide_prediction(
                location,
                cls.base_time + datetime.timedelta(minutes=minute),
                5.0
            )

    def _get_response_for_interval(self, interval_string):
        return self.client.get(
            self.BASE_PATH + 'liverpool/'
            '?start=2014-06-01T00:00:00Z'
            '&end=2014-06-03T00:00:00Z'
            '&interval={}'.format(interval_string)
        )

    def test_that_default_interval_is_one_minute(self):
        response = self.client.get(
            self.BASE_PATH + 'liverpool/'
            '?start=2014-06-01T00:00:00Z'
            '&end=2014-06-03T00:00:00Z'
        )
        sea_levels = decode_json(response.content)['sea_levels']
        assert_equal(60, len(sea_levels))

        assert_equal('2014-06-01T10:30:00Z', sea_levels[0]['datetime'])
        assert_equal('2014-06-01T10:31:00Z', sea_levels[1]['datetime'])
        assert_equal('2014-06-01T10:32:00Z', sea_levels[2]['datetime'])

    def test_that_non_integer_interval_gives_http_400(self):
        response = self._get_response_for_interval('foo')

        assert_equal(400, response.status_code)
        assert_equal(
            {'detail': 'Invalid interval: expected integer (minutes)'},
            decode_json(response.content))

    def test_that_interval_must_be_above_1(self):
        response = self._get_response_for_interval('0')
        assert_equal(400, response.status_code)

        assert_equal(
            {'detail': 'Invalid interval: must be between 1 and 60 minutes'},
            decode_json(response.content))

    def test_that_interval_must_be_below_61(self):
        response = self._get_response_for_interval('61')
        assert_equal(400, response.status_code)

        assert_equal(
            {'detail': 'Invalid interval: must be between 1 and 60 minutes'},
            decode_json(response.content))

    def test_that_five_minute_interval_works(self):
        response = self._get_response_for_interval('5')
        sea_levels = decode_json(response.content)['sea_levels']

        assert_equal(12, len(sea_levels))
        assert_equal('2014-06-01T10:30:00Z', sea_levels[0]['datetime'])
        assert_equal('2014-06-01T10:35:00Z', sea_levels[1]['datetime'])
        assert_equal('2014-06-01T10:40:00Z', sea_levels[2]['datetime'])

    def test_that_sixty_minute_interval_works(self):
        response = self._get_response_for_interval('60')
        sea_levels = decode_json(response.content)['sea_levels']

        assert_equal(1, len(sea_levels))
        assert_equal('2014-06-01T10:30:00Z', sea_levels[0]['datetime'])


class TestSeaLevelsViewOrderingResults(TestSeaLevelsViewBase):
    @classmethod
    def setUp(cls):
        cls.base_time = datetime.datetime(2014, 6, 1, 10, 30, tzinfo=pytz.UTC)
        cls.create_unordered_tide_level_entries()

    @classmethod
    def create_unordered_tide_level_entries(cls):
        location = Location.objects.get(slug='liverpool')
        for minute in [0, 4, 2, 3, 1]:
            create_tide_prediction(
                location,
                cls.base_time + datetime.timedelta(minutes=minute),
                5.0
            )

    def test_that_results_are_ordered_by_datetime(self):
        response = self.client.get(
            self.BASE_PATH + 'liverpool/'
            '?start=2014-06-01T00:00:00Z'
            '&end=2014-06-02T00:00:00Z'
        )
        data = decode_json(response.content)
        datetimes = [t['datetime'] for t in data['sea_levels']]
        assert_equal(
            [
                '2014-06-01T10:30:00Z',
                '2014-06-01T10:31:00Z',
                '2014-06-01T10:32:00Z',
                '2014-06-01T10:33:00Z',
                '2014-06-01T10:34:00Z'
            ],
            datetimes)
