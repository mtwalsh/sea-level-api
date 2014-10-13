import datetime

import pytz
from nose.tools import assert_equal, assert_is_instance, assert_raises
from freezegun import freeze_time
from django.test import TestCase

from api.apps.locations.models import Location
from ..alert_manager import (AlertType, disable_alert_until, enable_alert,
                             enable_all_alerts, is_alert_enabled,
                             alerts_enabled, alerts_disabled)

from ..models import LocationStatusConfig


BASE_DATE = datetime.datetime(2014, 11, 24, 10, 0, tzinfo=pytz.UTC)


class TestAlertManagerBase(TestCase):
    def setUp(self):
        self.liverpool = Location.objects.create(slug='liverpool')

    def tearDown(self):
        Location.objects.all().delete()
        LocationStatusConfig.objects.all().delete()

    def _disable(self, alert_type):
        disable_alert_until(self.liverpool, alert_type,
                            BASE_DATE + datetime.timedelta(hours=10))

    def _enable(self, alert_type):
        enable_alert(self.liverpool, alert_type)

    def _assert_enabled(self, alert_type):
        assert_equal(
            True, is_alert_enabled(self.liverpool, alert_type))

    def _assert_disabled(self, alert_type):
        assert_equal(
            False, is_alert_enabled(self.liverpool, alert_type))


class TestAlertManagerEnablingDisabling(TestAlertManagerBase):

    def test_that_disable_alert_until__cant_be_called_with_past_datetime(self):
        with freeze_time(BASE_DATE):
            assert_raises(
                AssertionError,
                lambda: disable_alert_until(
                    self.liverpool, AlertType.tide_predictions,
                    BASE_DATE - datetime.timedelta(hours=1)))

    def test_tide_predictions_alerts_can_be_disabled(self):
        self._assert_enabled(AlertType.tide_predictions)

        with freeze_time(BASE_DATE):
            self._disable(AlertType.tide_predictions)
            self._assert_disabled(AlertType.tide_predictions)

    def test_surge_predictions_alerts_can_be_disabled(self):
        self._assert_enabled(AlertType.surge_predictions)

        with freeze_time(BASE_DATE):
            self._disable(AlertType.surge_predictions)
            self._assert_disabled(AlertType.surge_predictions)

    def test_observations_alerts_can_be_disabled(self):
        self._assert_enabled(AlertType.observations)

        with freeze_time(BASE_DATE):
            self._disable(AlertType.observations)
            self._assert_disabled(AlertType.observations)

    def test_that_tide_predictions_alerts_can_be_re_enabled(self):
        with freeze_time(BASE_DATE):
            self._disable(AlertType.tide_predictions)

        self._enable(AlertType.tide_predictions)
        self._assert_enabled(AlertType.tide_predictions)

    def test_that_surge_predictions_alerts_can_be_re_enabled(self):
        with freeze_time(BASE_DATE):
            self._disable(AlertType.surge_predictions)

        self._enable(AlertType.surge_predictions)
        self._assert_enabled(AlertType.surge_predictions)

    def test_that_observations_alerts_can_be_re_enabled(self):
        with freeze_time(BASE_DATE):
            self._disable(AlertType.observations)

        self._enable(AlertType.observations)
        self._assert_enabled(AlertType.observations)

    def test_that__enable_all_alerts__actually_enables_all_alerts(self):
        with freeze_time(BASE_DATE):
            self._disable(AlertType.tide_predictions)
            self._disable(AlertType.surge_predictions)
            self._disable(AlertType.observations)
        enable_all_alerts(self.liverpool)

        self._assert_enabled(AlertType.tide_predictions)
        self._assert_enabled(AlertType.surge_predictions)
        self._assert_enabled(AlertType.observations)

    def test_that__alerts_disabled___returns_correct_set(self):
        with freeze_time(BASE_DATE):
            self._disable(AlertType.tide_predictions)

        assert_equal(
            set([AlertType.tide_predictions]),
            alerts_disabled(self.liverpool))

    def test_that__alerts_enabled__returns_correct_set(self):
        with freeze_time(BASE_DATE):
            self._disable(AlertType.tide_predictions)

        assert_equal(
            set([AlertType.surge_predictions, AlertType.observations]),
            alerts_enabled(self.liverpool))


class TestAlertManagerImplementation(TestAlertManagerBase):

    def _assert_no_config(self):
        assert_equal(0, LocationStatusConfig.objects.all().count())

    def _assert_has_config(self):
        assert_equal(1, LocationStatusConfig.objects.all().count())

    def test_that__is_alert_enabled__works_without_prior_config(self):
        self._assert_no_config()
        is_alert_enabled(self.liverpool, AlertType.tide_predictions)
        self._assert_has_config()

    def test_that__disable_alert_until__works_without_prior_config(self):
        self._assert_no_config()
        self._disable(AlertType.tide_predictions)
        self._assert_has_config()

    def test_that__enable_alert__works_without_prior_config(self):
        self._assert_no_config()
        enable_alert(self.liverpool, AlertType.tide_predictions)
        self._assert_has_config()

    def test_that__enable_all_alerts__works_without_prior_config(self):
        self._assert_no_config()
        enable_all_alerts(self.liverpool)
        self._assert_has_config()

    def test_that_none_value_for__disabled_until__is_ok(self):
        LocationStatusConfig.objects.create(
            location=self.liverpool,
            tide_predictions_alerts_disabled_until=None)
        assert_equal(
            True,
            is_alert_enabled(self.liverpool, AlertType.tide_predictions))

    def test_that_disabled_alerts_sets__disabled_until__to_datetime(self):
        self._disable(AlertType.tide_predictions)
        config = LocationStatusConfig.objects.get(location__slug='liverpool')
        assert_is_instance(config.tide_predictions_alerts_disabled_until,
                           datetime.datetime)

    def test_that_enable_alerts_sets__disabled_until__to_none(self):
        self._disable(AlertType.tide_predictions)
        self._enable(AlertType.tide_predictions)

        config = LocationStatusConfig.objects.get(location__slug='liverpool')
        assert_equal(None, config.tide_predictions_alerts_disabled_until)

    def test_that_expired__disabled_until__gets_set_to_none(self):
        yesterday = BASE_DATE - datetime.timedelta(days=1)

        with freeze_time(yesterday):
            disable_alert_until(self.liverpool, AlertType.tide_predictions,
                                BASE_DATE)

        with freeze_time(BASE_DATE):  # now it's expired
            self._assert_enabled(AlertType.tide_predictions)

        config = LocationStatusConfig.objects.get(location__slug='liverpool')
        assert_equal(None, config.tide_predictions_alerts_disabled_until)
