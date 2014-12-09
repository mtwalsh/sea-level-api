from nose.tools import assert_equal
from freezegun import freeze_time

from api.libs.test_utils import decode_json

from .test_tide_windows import TestTideWindowsViewBase


class TestTideWindowsNow(TestTideWindowsViewBase):
    """
    Test that the `/now/` endpoint searches from now until now + 24 hours.
    """

    @classmethod
    def setUp(cls):
        cls.create_two_days_of_tide()

    @classmethod
    def create_two_days_of_tide(cls):
        day = 86400

        cls.create_predictions([
            (-5, 4.0),
            (-4, 4.51),
            (-3, 5.00),
            (-2, 5.10, True),
            (-1, 3.0),

            (0, 4.50),
            (1, 4.75),
            (2, 5.00),
            (3, 5.10, True),
            (4, 4.60),
            (5, 4.55),

            (day + 0, 4.50),
            (day + 1, 4.75),
            (day + 2, 5.00),
            (day + 3, 5.10, True),
            (day + 4, 4.60),
            (day + 5, 4.55),
        ])

    def test_that_now_endpoint_returns_http_200_ok(self):
        response = self.client.get(
            self.BASE_PATH + 'liverpool/now/?tide_level=4.5')
        assert_equal(200, response.status_code)

    def test_that_now_searches_from_now_to_24_hours(self):
        with freeze_time("2014-06-01T10:00:00Z"):
            response = self.client.get(
                self.BASE_PATH + 'liverpool/now/?tide_level=4.5')

        data = decode_json(response.content)
        assert_equal(1, len(data['tide_windows']))
        assert_equal(
            ('2014-06-01T10:00:00Z', 4.50,
             '2014-06-01T10:05:00Z', 4.55,
             '2014-06-01T10:03:00Z', 5.1,
             360),
            self.parse_window(data['tide_windows'][0])
        )
