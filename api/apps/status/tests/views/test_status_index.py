import datetime
import pytz

from freezegun import freeze_time

from django.test import TestCase
from nose.tools import assert_equal


from api.apps.observations.models import Observation
from api.apps.observations.utils import create_observation
from api.apps.predictions.models import Prediction
from api.apps.predictions.utils import create_prediction

from api.apps.locations.models import Location

from api.apps.status.views.status_index import (
    check_tide_predictions, check_observations)


class TestStatusIndexView(TestCase):
    BASE_PATH = '/1/_status/'

    def setUp(self):
        self.liv = Location.objects.create(slug='liverpool', name='Liverpool')
        self.base_time = datetime.datetime(
            2014, 8, 1, 10, 0, 0, tzinfo=pytz.UTC)

    def _setup_all_ok(self):
        create_prediction(
            self.liv,
            self.base_time + datetime.timedelta(days=31),
            5.0)
        create_observation(
            self.liv,
            self.base_time - datetime.timedelta(minutes=10),
            4.5,
            True)

    def _setup_not_ok(self):
        Prediction.objects.all().delete()
        Observation.objects.all().delete()

    def test_that_status_page_has_api_status_ok_when_all_ok(self):
        self._setup_all_ok()
        with freeze_time(self.base_time):
            response = self.client.get(self.BASE_PATH)
        self.assertContains(response, 'API Status: OK', status_code=200)

    def test_that_status_page_has_api_status_error_when_something_not_ok(self):
        self._setup_not_ok()
        with freeze_time(self.base_time):
            response = self.client.get(self.BASE_PATH)
        self.assertContains(response, 'API Status: ERROR', status_code=500)


class TestCheckBase(TestCase):
    fixtures = ['api/apps/locations/fixtures/two_locations.json']

    def setUp(self):
        self.liverpool = Location.objects.get(slug='liverpool')
        self.southampton = Location.objects.get(slug='southampton')
        self.base_time = datetime.datetime(
            2014, 8, 1, 10, 0, 0, tzinfo=pytz.UTC)


class TestCheckTidePredictions(TestCheckBase):
    def test_that_tide_predictions_further_than_one_month_is_ok(self):
        create_prediction(
            self.liverpool,
            self.base_time + datetime.timedelta(days=31),
            10.0)

        with freeze_time(self.base_time):
            (ok, text) = check_tide_predictions(self.liverpool)

        assert_equal(True, ok)
        assert_equal('OK', text)

    def test_that_tide_predictions_less_than_one_month_not_ok(self):
        create_prediction(
            self.liverpool,
            self.base_time + datetime.timedelta(days=29),
            10.0)

        with freeze_time(self.base_time):
            (ok, text) = check_tide_predictions(self.liverpool)

        assert_equal(False, ok)
        assert_equal('< 30 days left', text)

    def test_that_predictions_for_liverpool_dont_affect_southampton(self):
        create_prediction(
            self.liverpool,
            self.base_time + datetime.timedelta(days=31),
            10.0)

        with freeze_time(self.base_time):
            (ok, text) = check_tide_predictions(self.southampton)

        assert_equal(False, ok)
        assert_equal('< 30 days left', text)


class TestCheckObservations(TestCheckBase):
    def test_that_observations_more_recent_than_one_hour_are_ok(self):
        create_observation(
            self.liverpool,
            self.base_time - datetime.timedelta(minutes=59),
            10.0, True)

        with freeze_time(self.base_time):
            (ok, text) = check_observations(self.liverpool)

        assert_equal(True, ok)
        assert_equal('OK', text)

    def test_that_observations_over_one_hour_old_not_ok(self):
        create_observation(
            self.liverpool,
            self.base_time - datetime.timedelta(minutes=61),
            10.0, True)

        with freeze_time(self.base_time):
            (ok, text) = check_observations(self.liverpool)

        assert_equal(False, ok)
        assert_equal('> 1 hour old', text)

    def test_that_observations_from_liverpool_dont_affect_southampton(self):
        create_observation(
            self.liverpool,
            self.base_time - datetime.timedelta(minutes=59),
            10.0, True)

        with freeze_time(self.base_time):
            (ok, text) = check_observations(self.southampton)

        assert_equal(False, ok)
        assert_equal('> 1 hour old', text)


class TestCheckSurgePredictions(TestCheckBase):
    pass
