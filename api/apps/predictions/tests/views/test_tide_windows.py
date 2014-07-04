import datetime

import pytz

from django.test import TestCase

from nose.tools import assert_equal, assert_in

from api.apps.predictions.models import Prediction
from api.apps.locations.models import Location
from api.libs.test_utils import decode_json

from .test_location_parsing import LocationParsingTestMixin
from .test_time_parsing import TimeParsingTestMixin


class TestTideWindowsViewBase(TestCase):
    PATH = '/1/predictions/tide-windows/'


class TestTideWindowsView(TestTideWindowsViewBase, LocationParsingTestMixin,
                          TimeParsingTestMixin):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
        'api/apps/predictions/fixtures/predictions_two_locations.json',
    ]

    def test_that_missing_tide_level_param_gives_400_error(self):
        response = self.client.get(
            self.PATH + 'liverpool/'
            '?start=2014-06-17T09:00:00Z'
            '&end=2014-06-17T09:05:00Z')
        data = decode_json(response.content)
        assert_equal(400, response.status_code)
        assert_equal(
            {'detail': 'Missing required query parameter `tide_level`'},
            data)

    def test_that_envelope_has_tide_windows_field(self):
        response = self.client.get(
            self.PATH + 'liverpool/'
            '?start=2014-06-17T00:00:00Z'
            '&end=2014-06-18T00:00:00Z'
            '&tide_level=10.7')
        data = decode_json(response.content)
        assert_in('tide_windows', data)

    def test_that_tide_window_records_have_correct_structure(self):
        response = self.client.get(
            self.PATH + 'liverpool/'
            '?start=2014-06-17T00:00:00Z'
            '&end=2014-06-18T00:00:00Z'
            '&tide_level=10.7')
        data = decode_json(response.content)
        tide_windows = data['tide_windows']
        expected = {
            'start': {
                'datetime': '2014-06-17T09:01:00Z',
                'tide_level': 10.8
            },
            'end': {
                'datetime': '2014-06-17T09:02:00Z',
                'tide_level': 10.9
            },
            'duration': {
                'total_seconds': 120
            }
        }
        assert_equal(expected, tide_windows[0])


class TestTideWindowsCalculationsView(TestTideWindowsViewBase):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
    ]

    @classmethod
    def setUp(cls):
        cls.create_double_peaked_tide()

    @classmethod
    def create_double_peaked_tide(cls):
        location = Location.objects.get(slug='liverpool')

        cls.base_time = datetime.datetime(2014, 6, 1, 10, 00, tzinfo=pytz.UTC)

        for minute, level in [
            (0, 4.50),
            (1, 4.75),
            (2, 5.00),
            (3, 5.25),
            (4, 5.50),
            (5, 5.75),
            (6, 6.00),  # peak
            (7, 5.60),
            (8, 5.49),
            (9, 5.25),
            (10, 5.00),  # trough
            (11, 5.25),
            (12, 5.49),  # peak
            (13, 5.25),
            (14, 5.00),
            (15, 4.75),
            (16, 4.50)
        ]:

            Prediction.objects.create(
                location=location,
                datetime=cls.base_time + datetime.timedelta(minutes=minute),
                tide_level=level
            )

    def test_that_single_window_is_correctly_identified(self):
        response = self.client.get(
            self.PATH + 'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-02T11:00:00Z'
            '&tide_level=5.5'
        )
        data = decode_json(response.content)
        assert_equal([
            {
                'start': {
                    'datetime': '2014-06-01T10:04:00Z',
                    'tide_level': 5.50,
                },
                'end': {
                    'datetime': '2014-06-01T10:07:00Z',
                    'tide_level': 5.60,
                },
                'duration': {
                    'total_seconds': 240,
                }
            }],
            data['tide_windows']
        )

    def test_that_double_window_is_correctly_identified(self):
        response = self.client.get(
            self.PATH + 'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-02T11:00:00Z'
            '&tide_level=5.1'
        )
        data = decode_json(response.content)
        assert_equal([
            {
                'start': {
                    'datetime': '2014-06-01T10:03:00Z',
                    'tide_level': 5.25,
                },
                'end': {
                    'datetime': '2014-06-01T10:09:00Z',
                    'tide_level': 5.25,
                },
                'duration': {
                    'total_seconds': 420,
                }
            },
            {
                'start': {
                    'datetime': '2014-06-01T10:11:00Z',
                    'tide_level': 5.25,
                },
                'end': {
                    'datetime': '2014-06-01T10:13:00Z',
                    'tide_level': 5.25,
                },
                'duration': {
                    'total_seconds': 180,
                }
            },
        ],
            data['tide_windows']
        )

    def test_that_no_tidal_window_returned_if_tide_is_never_above_height(self):
        response = self.client.get(
            self.PATH + 'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-02T11:00:00Z'
            '&tide_level=6.1'
        )
        data = decode_json(response.content)
        assert_equal([], data['tide_windows'])
