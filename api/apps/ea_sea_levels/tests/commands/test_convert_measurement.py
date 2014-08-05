import datetime
import pytz
import sys

from django.test import TestCase

from nose.tools import assert_equal, assert_in

from api.apps.observations.models import Observation
from api.apps.observations.utils import create_observation

from api.apps.ea_sea_levels.models import Measurement, Station
from api.apps.ea_sea_levels.management.commands.convert_measurements import (
    make_linear_interpolations, update_observations)


class TestUpdateObservations(TestCase):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
        'api/apps/ea_sea_levels/fixtures/liverpool_station.json',
    ]

    @classmethod
    def setUp(cls):
        Measurement.objects.all().delete()
        Observation.objects.all().delete()
        cls.station = Station.objects.get(station_name='Liverpool')

        cls.datetime_1 = datetime.datetime(2014, 8, 3, 10, 0, tzinfo=pytz.UTC)
        cls.datetime_2 = datetime.datetime(2014, 8, 3, 10, 15, tzinfo=pytz.UTC)

    @classmethod
    def make_two_measurements(cls):
        Measurement.objects.create(
            station=cls.station,
            datetime=cls.datetime_1,
            measurement=10)

        Measurement.objects.create(
            station=cls.station,
            datetime=cls.datetime_2,
            measurement=5)

    def test_that_no_measurements_does_nothing(self):
        update_observations(self.station, sys.stdout)
        assert_equal(0, Observation.objects.all().count())

    def test_that_up_to_date_observations_does_nothing(self):
        self.make_two_measurements()
        create_observation(self.station.location, self.datetime_2, 10, False)
        update_observations(self.station, sys.stdout)
        assert_equal(1, Observation.objects.all().count())

    def test_two_measurements_and_no_measurements_does_conversions(self):
        self.make_two_measurements()
        update_observations(self.station, sys.stdout)
        observations = Observation.objects.all()
        assert_equal(16, observations.count())
        assert_equal(self.datetime_1, observations[0].minute.datetime)
        assert_equal(self.datetime_2, list(observations)[-1].minute.datetime)

    def test_that_conversions_are_correct_with_4_93_offset(self):
        self.make_two_measurements()
        update_observations(self.station, sys.stdout)
        assert_equal([
            14.93,
            14.6,
            14.26,
            13.93,
            13.6,
            13.26,
            12.93,
            12.6,
            12.26,
            11.93,
            11.6,
            11.26,
            10.93,
            10.6,
            10.26,
            9.93],
            [o.sea_level for o in Observation.objects.all()])


class TestMakeLinearInterpolations(TestCase):
    fixtures = [
        'api/apps/locations/fixtures/two_locations.json',
        'api/apps/ea_sea_levels/fixtures/liverpool_station.json',
    ]

    @classmethod
    def make_datetime(cls, minute):
        return cls.base_datetime + datetime.timedelta(minutes=minute)

    @classmethod
    def setUp(cls):

        station = Station.objects.get(station_name='Liverpool')
        cls.base_datetime = datetime.datetime(
            2013, 8, 1, 10, 0, tzinfo=pytz.UTC)
        measurements = [
            (0, 5.0),
            (15, 10.0),
            (30, 20.0),
            # missing 45
            (60, 10),
            (74, 10)]

        for minute, height in measurements:
            dt = cls.make_datetime(minute)
            Measurement.objects.create(
                datetime=dt, measurement=height, station=station)

    def test_that_start_measurement_datetime_is_inclusive(self):
        interpolations = list(make_linear_interpolations(
            start=self.make_datetime(0),
            end=self.make_datetime(24 * 60)))
        assert_in(
            self.base_datetime,
            [i[0] for i in interpolations]
        )

    def test_that_end_measurement_datetime_is_inclusive(self):
        interpolations = list(make_linear_interpolations(
            start=self.make_datetime(-24 * 60),
            end=self.make_datetime(30)))
        assert_in(
            self.base_datetime,
            [i[0] for i in interpolations]
        )

    def test_that_interpolations_wont_occur_for_more_than_15_mins(self):
        # But we should still convert the *actual* measurements even though
        # we don't interpolate between them.
        interpolations = list(make_linear_interpolations(
            start=self.make_datetime(30),
            end=self.make_datetime(60)))
        assert_equal(2, len(interpolations))

    def test_that_interpolations_occur_for_15_mins(self):
        interpolations = list(make_linear_interpolations(
            start=self.make_datetime(15),
            end=self.make_datetime(30)))
        assert_equal(16, len(interpolations))

    def test_that_interpolations_occur_for_14_mins(self):
        interpolations = list(make_linear_interpolations(
            start=self.make_datetime(60),
            end=self.make_datetime(74)))
        assert_equal(15, len(interpolations))

    def test_that_two_measurements_results_in_31_observations(self):
        interpolations = list(make_linear_interpolations(
            start=self.make_datetime(0),
            end=self.make_datetime(30)))
        assert_equal(31, len(interpolations))

    def test_that_datetimes_are_correct(self):
        interpolations = list(make_linear_interpolations(
            start=self.make_datetime(0),
            end=self.make_datetime(30)))
        assert_equal(
            [self.make_datetime(x) for x in range(31)],
            [i[0] for i in interpolations])

    def test_that_interpolations_are_tagged_as_interpolations_correctly(self):
        interpolations = list(make_linear_interpolations(
            start=self.make_datetime(0),
            end=self.make_datetime(30)))
        fourteen_trues = 14 * [True]
        assert_equal(
            [False] + fourteen_trues + [False] + fourteen_trues + [False],
            [i[2] for i in interpolations])

    def test_that_linear_interpolations_are_correct(self):
        interpolations = list(make_linear_interpolations(
            start=self.make_datetime(0),
            end=self.make_datetime(30)))
        assert_equal(
            [5.0, 5.33, 5.67, 6.0, 6.33,
             6.67, 7.0, 7.33, 7.67, 8.0,
             8.33, 8.67, 9.0, 9.33, 9.67,
             10.0, 10.67, 11.33, 12.0, 12.67,
             13.33, 14.0, 14.67, 15.33, 16.0,
             16.67, 17.33, 18.0, 18.67, 19.33,
             20.0],
            [i[1] for i in interpolations])
