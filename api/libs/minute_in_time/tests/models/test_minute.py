import datetime
import pytz

from django.test import TestCase
from nose.tools import assert_equal, assert_raises

from api.libs.minute_in_time.models import Minute


class TestMinuteModel(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unrounded_datetime = datetime.datetime(
            2014, 8, 3, 17, 12, 56, 2345, tzinfo=pytz.UTC)
        cls.rounded_datetime = datetime.datetime(
            2014, 8, 3, 17, 12, 0, 0, tzinfo=pytz.UTC)
        cls.london_datetime = cls.rounded_datetime.astimezone(
            pytz.timezone('Europe/London'))

    def test_that_datetimes_are_rounded_to_nearest_minute(self):
        minute = Minute.objects.create(datetime=self.unrounded_datetime)
        assert_equal(
            self.rounded_datetime,
            minute.datetime)

    def test_that_naive_datetime_not_allowed(self):
        naive_datetime = datetime.datetime(2014, 8, 3, 17, 12)
        assert_raises(
            ValueError,
            lambda: Minute.objects.create(datetime=naive_datetime))

    def test_that_timezone_not_django_utc_is_not_allowed(self):
        assert_raises(
            ValueError,
            lambda: Minute.objects.create(datetime=self.london_datetime))
