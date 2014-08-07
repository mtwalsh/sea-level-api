import datetime

import pytz

from nose.tools import assert_equal
from freezegun import freeze_time

from api.apps.predictions.utils import create_prediction
from api.apps.locations.models import Location
from api.libs.test_utils import decode_json

from .test_tide_levels import TestTideLevelsViewBase


class TestTideLevelsNow(TestTideLevelsViewBase):
    """
    Test that the `/now/` endpoint searches from now until now + 24 hours.
    """
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
    ]

    @classmethod
    def setUp(cls):
        cls.create_over_twenty_four_hours_of_tide()

    @classmethod
    def create_over_twenty_four_hours_of_tide(cls):
        location = Location.objects.get(slug='liverpool')

        cls.base_time = datetime.datetime(2014, 6, 1, 10, 00, tzinfo=pytz.UTC)

        day = 86400

        minutes = [-10, -9, -8,
                   0, 1, 2, 3, 4,
                   day + 1, day + 2, day + 3]

        for minute in minutes:
            create_prediction(
                location,
                cls.base_time + datetime.timedelta(minutes=minute),
                5
            )

    def test_that_now_endpoint_returns_http_200_ok(self):
        response = self.client.get(
            self.PATH + 'liverpool/now/')
        assert_equal(200, response.status_code)

    def test_that_now_searches_from_now_to_24_hours(self):
        with freeze_time("2014-06-01T10:00:00Z"):
            response = self.client.get(
                self.PATH + 'liverpool/now/')

        data = decode_json(response.content)
        assert_equal(5, len(data['tide_levels']))
        assert_equal('2014-06-01T10:00:00Z',
                     data['tide_levels'][0]['datetime'])
        assert_equal('2014-06-01T10:04:00Z',
                     data['tide_levels'][-1]['datetime'])
