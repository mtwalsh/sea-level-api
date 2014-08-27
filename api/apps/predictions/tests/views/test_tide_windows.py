import datetime

import pytz

from django.test import TestCase

from nose.tools import assert_equal, assert_in

from api.apps.predictions.models import TidePrediction
from api.apps.predictions.utils import create_tide_prediction
from api.apps.locations.models import Location
from api.libs.minute_in_time.models import Minute
from api.libs.test_utils import decode_json

from .test_location_parsing import LocationParsingTestMixin
from .test_time_parsing import TimeParsingTestMixin
from .test_database_queries import SingleDatabaseQueryTestMixin


class TestTideWindowsViewBase(TestCase):
    BASE_PATH = '/1/predictions/tide-windows/'
    EXAMPLE_FULL_PATH = (
        BASE_PATH + 'liverpool/'
        '?start=2014-06-17T00:00:00Z'
        '&end=2014-06-18T00:00:00Z'
        '&tide_level=10.7')

    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
    ]

    @classmethod
    def setUp(cls):
        cls.location = Location.objects.get(slug='liverpool')
        cls.base_time = datetime.datetime(2014, 6, 1, 10, 00, tzinfo=pytz.UTC)

    @classmethod
    def create_predictions(cls, minutes_and_levels):
        for minute, level in minutes_and_levels:
            create_tide_prediction(
                cls.location,
                cls.base_time + datetime.timedelta(minutes=minute),
                level
            )

    @classmethod
    def bulk_create_predictions(cls, minutes_and_levels):
        """
        There must not be any overlapping Minute objects.
        """
        minutes_and_levels = list(minutes_and_levels)
        Minute.objects.bulk_create(
            Minute(datetime=cls.to_datetime(m)) for m, _ in minutes_and_levels)

        minute_cache = {m.datetime: m for m in Minute.objects.all()}
        TidePrediction.objects.bulk_create(
            TidePrediction(location=cls.location,
                           minute=minute_cache[cls.to_datetime(m)],
                           tide_level=l)
            for m, l in minutes_and_levels)

    @classmethod
    def to_datetime(cls, num_minutes):
        return cls.base_time + datetime.timedelta(minutes=num_minutes)

    @staticmethod
    def parse_window(data):
        return (
            data['start']['datetime'],
            data['start']['tide_level'],
            data['end']['datetime'],
            data['end']['tide_level'],
            data['duration']['total_seconds']
        )

    def get_tide_windows(self, path):
        response = self.client.get(self.BASE_PATH + path)
        data = decode_json(response.content)
        return data['tide_windows']


class TestTideWindowsView(TestTideWindowsViewBase, LocationParsingTestMixin,
                          TimeParsingTestMixin, SingleDatabaseQueryTestMixin):
    fixtures = TestTideWindowsViewBase.fixtures + [
        'api/apps/predictions/fixtures/predictions_two_locations.json',
    ]

    def test_that_missing_tide_level_param_gives_400_error(self):
        response = self.client.get(
            self.BASE_PATH + 'liverpool/'
            '?start=2014-06-17T09:00:00Z'
            '&end=2014-06-17T09:05:00Z')
        data = decode_json(response.content)
        assert_equal(400, response.status_code)
        assert_equal(
            {'detail': 'Missing required query parameter `tide_level`'},
            data)

    def test_that_envelope_has_tide_windows_field(self):
        response = self.client.get(self.EXAMPLE_FULL_PATH)
        data = decode_json(response.content)
        assert_in('tide_windows', data)

    def test_that_tide_window_records_have_correct_structure(self):
        response = self.client.get(self.EXAMPLE_FULL_PATH)
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


class TestTideWindowsSimpleCalculations(TestTideWindowsViewBase):
    @classmethod
    def setUp(cls):
        super(TestTideWindowsSimpleCalculations, cls).setUp()
        cls.create_predictions([
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
        ])

    def test_that_single_window_is_correctly_identified(self):
        tide_windows = self.get_tide_windows(
            'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-02T11:00:00Z'
            '&tide_level=5.5')
        assert_equal(1, len(tide_windows))
        assert_equal(
            ('2014-06-01T10:04:00Z', 5.50, '2014-06-01T10:07:00Z', 5.60, 240),
            self.parse_window(tide_windows[0]))

    def test_that_double_window_is_correctly_identified(self):
        tide_windows = self.get_tide_windows(
            'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-02T11:00:00Z'
            '&tide_level=5.1')
        assert_equal(2, len(tide_windows))

        assert_equal(
            ('2014-06-01T10:03:00Z', 5.25, '2014-06-01T10:09:00Z', 5.25, 420),
            self.parse_window(tide_windows[0]))

        assert_equal(
            ('2014-06-01T10:11:00Z', 5.25, '2014-06-01T10:13:00Z', 5.25, 180),
            self.parse_window(tide_windows[1]))

    def test_that_no_tidal_window_returned_if_tide_is_never_above_height(self):
        tide_windows = self.get_tide_windows(
            'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-02T11:00:00Z'
            '&tide_level=6.1')
        assert_equal([], tide_windows)


class TestTideWindowsOverlappingStartTime(TestTideWindowsViewBase):
    def test_that_a_tide_window_overlapping_start_time_has_correct_start(self):
        #                   start      end
        #                    |          |
        #                /------\
        #
        # expected:      ^      ^
        self.create_predictions([
            (-4, 4),
            (-3, 5),
            (-2, 6),
            (-1, 6),
            (0, 6),
            (1, 6),
            (2, 6),
            (3, 6),
            (4, 5),
            (5, 4),
        ])

        tide_windows = self.get_tide_windows(
            'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-02T11:00:00Z'
            '&tide_level=5')
        assert_equal(1, len(tide_windows))

        assert_equal(
            ('2014-06-01T09:57:00Z', 5.0, '2014-06-01T10:04:00Z', 5.0, 480),
            self.parse_window(tide_windows[0]))


class TestTideWindowsOverlappingEndTime(TestTideWindowsViewBase):
    def test_that_a_tide_window_overlapping_end_time_has_correct_end(self):
        #       start      end
        #        |          |
        #                /------\
        #
        # expected:      ^      ^

        self.create_predictions([
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 6),
            (4, 6),
            (5, 6),
            (6, 6),
            (7, 6),
            (8, 5),
            (9, 4),
        ])

        tide_windows = self.get_tide_windows(
            'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-01T10:05:00Z'
            '&tide_level=5')
        assert_equal(1, len(tide_windows))

        assert_equal(
            ('2014-06-01T10:01:00Z', 5, '2014-06-01T10:08:00Z', 5, 480),
            self.parse_window(tide_windows[0]))


class TestTideWindowsFullyBeforeStart(TestTideWindowsViewBase):
    def test_that_a_tide_window_fully_before_start_is_ignored(self):
        # start-24h    start      end
        #   |            |          |
        #      /----\
        #
        # expected:      no windows

        self.create_predictions([
            (-10, 6),
            (-9, 6),
            (-8, 6),
            (-7, 6),
            (-6, 6),
            (-5, 6),
            (-4, 2),
            (-3, 2),
            (-2, 2),
            (-1, 2),
        ])

        tide_windows = self.get_tide_windows(
            'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-01T10:05:00Z'
            '&tide_level=5')
        assert_equal(0, len(tide_windows))


class TestTideWindowsFullyAfterEnd(TestTideWindowsViewBase):
    def test_that_a_tide_window_fully_after_end_is_ignored(self):
        # start      end          end+24h
        #   |          |           |
        #                  /----\
        #
        # expected:      no windows

        self.create_predictions([
            (10, 6),
            (11, 6),
            (12, 6),
            (13, 6),
            (14, 6),
            (15, 6),
        ])

        tide_windows = self.get_tide_windows(
            'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-01T10:05:00Z'
            '&tide_level=5')
        assert_equal(0, len(tide_windows))


class TestTideWindowsExtendingLongPastStart(TestTideWindowsViewBase):
    def test_that_a_tide_window_going_24_hours_before_start_is_squashed(self):
        # start-24h     start       end
        #   |             |          |
        # -------------------\
        #
        # expected:       ^  ^

        self.bulk_create_predictions(
            (minute, 6) for minute in range(-25 * 60, 0, 1))

        self.create_predictions([
            (0, 6),
            (1, 6),
            (2, 6),
            (3, 6),
            (4, 5),
            (5, 4),
            (6, 3),
        ])

        tide_windows = self.get_tide_windows(
            'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-01T12:00:00Z'
            '&tide_level=6')
        assert_equal(1, len(tide_windows))

        assert_equal(
            ('2014-06-01T10:00:00Z', 6.0, '2014-06-01T10:03:00Z', 6.0, 240),
            self.parse_window(tide_windows[0]))


class TestTideWindowsExtendingLongPastEnd(TestTideWindowsViewBase):
    def test_that_a_tide_window_going_24_hours_after_end_is_squashed(self):
        #               start       end          end+24hours
        #                 |          |             |
        #                        /--------------------------
        #
        # expected:              ^   ^

        self.create_predictions([
            (0, 3),
            (1, 6),
            (2, 6),
            (3, 6),
            (4, 6),
        ])

        self.bulk_create_predictions(
            (minute, 6) for minute in range(5, 5 + 25 * 600, 1))
        tide_windows = self.get_tide_windows(
            'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-01T10:04:00Z'
            '&tide_level=6')
        assert_equal(1, len(tide_windows))

        assert_equal(
            ('2014-06-01T10:01:00Z', 6.0, '2014-06-01T10:04:00Z', 6.0, 240),
            self.parse_window(tide_windows[0]))


class TestTideWindowsExtendingLongPastStartAndEnd(TestTideWindowsViewBase):
    def test_that_a_tide_thats_always_above_start_and_end_is_squashed(self):
        # start-24h     start       end          end+24hours
        #  |              |          |             |
        # /--------------------------------------------------\
        #
        # expected:       ^          ^

        self.bulk_create_predictions(
            (minute, 6) for minute in range(-25 * 600, 5 + 25 * 600, 1))
        tide_windows = self.get_tide_windows(
            'liverpool/'
            '?start=2014-06-01T10:00:00Z'
            '&end=2014-06-01T10:05:00Z'
            '&tide_level=6')
        assert_equal(1, len(tide_windows))

        assert_equal(
            ('2014-06-01T10:00:00Z', 6.0, '2014-06-01T10:05:00Z', 6.0, 360),
            self.parse_window(tide_windows[0]))
