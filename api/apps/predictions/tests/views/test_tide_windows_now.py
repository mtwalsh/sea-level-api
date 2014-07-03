import datetime
import json

import pytz

from nose.tools import assert_equal
from freezegun import freeze_time

from api.apps.predictions.models import Prediction
from api.apps.locations.models import Location

from .test_tide_windows import TestTideWindowsViewBase


class TestTideWindowsNow(TestTideWindowsViewBase):
    """
    Test that the `/now/` endpoint searches from now until now + 24 hours.
    """
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
    ]

    @classmethod
    def setUp(cls):
        cls.create_two_days_of_tide()

    @classmethod
    def create_two_days_of_tide(cls):
        location = Location.objects.get(slug='liverpool')

        cls.base_time = datetime.datetime(2014, 6, 1, 10, 00, tzinfo=pytz.UTC)

        day = 86400

        for minute, level in [
            (-5, 4.50),
            (-4, 4.75),
            (-3, 5.00),
            (-2, 5.10),
            (-1, 4.60),

            (0, 4.50),
            (1, 4.75),
            (2, 5.00),
            (3, 5.10),
            (4, 4.60),
            (5, 4.55),

            (day + 0, 4.50),
            (day + 1, 4.75),
            (day + 2, 5.00),
            (day + 3, 5.10),
            (day + 4, 4.60),
            (day + 5, 4.55),
        ]:

            Prediction.objects.create(
                location=location,
                datetime=cls.base_time + datetime.timedelta(minutes=minute),
                tide_level=level
            )

    def test_that_now_endpoint_returns_http_200_ok(self):
        response = self.client.get(
            self.PATH + 'liverpool/now/?tide_level=4.5')
        print(response.content)
        assert_equal(200, response.status_code)

    def test_that_windows_start_now_and_end_in_24_hours(self):
        with freeze_time("2014-06-01T10:00:00Z"):
            response = self.client.get(
                self.PATH + 'liverpool/now/?tide_level=4.5')

        data = json.loads(response.content)
        assert_equal(1, len(data['tide_windows']))
        assert_equal(
            {
                'start': {
                    'datetime': '2014-06-01T10:00:00Z',
                    'tide_level': 4.50,
                },
                'end': {
                    'datetime': '2014-06-01T10:05:00Z',
                    'tide_level': 4.55,
                },
                'duration': {
                    'total_seconds': 360,
                }
            },
            data['tide_windows'][0]
        )
