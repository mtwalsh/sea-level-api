import datetime
import pytz

from nose.tools import assert_equal, assert_raises

from django.test import TestCase

from api.apps.predictions.views.helpers import split_prediction_windows


class FakeMinute(object):
    def __init__(self, datetime):
        self.datetime = datetime


class FakePrediction(object):
    """
    Lightweight pretend Prediction object for testing calculations without
    hitting the database.
    """
    def __init__(self, minute):
        self.minute = FakeMinute(
            TestSplitPrediction.BASE_DATETIME.replace(minute=minute))


class TestSplitPrediction(TestCase):
    BASE_DATETIME = datetime.datetime(2013, 1, 1, 10, 0, 0, tzinfo=pytz.UTC)

    @classmethod
    def _to_mins(cls, dt):
        return (dt - cls.BASE_DATETIME).total_seconds() / 60

    def _split_these_minutes(self, minutes):
        predictions = [FakePrediction(m) for m in minutes]
        return [(self._to_mins(start.minute.datetime),
                 self._to_mins(end.minute.datetime))
                for start, end in split_prediction_windows(predictions)]

    def test_split_prediction_windows_splits_single_window(self):
        assert_equal([
            (2, 4),
        ],
            self._split_these_minutes([2, 3, 4])
        )

    def test_that_it_splits_window_with_only_two_predictions(self):
        assert_equal([
            (2, 3),
        ],
            self._split_these_minutes([2, 3])
        )

    def test_that_it_splits_multiple_windows_correctly(self):
        assert_equal([
            (2, 4),
            (10, 12),
            (25, 26),
        ],
            self._split_these_minutes([2, 3, 4, 10, 11, 12, 25, 26])
        )

    def test_that_it_ignores_single_predictions_at_start(self):
        assert_equal([
            (10, 13),
        ],
            self._split_these_minutes([3, 10, 11, 12, 13])
        )

    def test_that_it_ignores_single_predictions_at_end(self):
        assert_equal([
            (10, 13),
        ],
            self._split_these_minutes([10, 11, 12, 13, 34])
        )

    def test_that_it_ignores_single_predictions_in_middle(self):
        assert_equal([
            (10, 12),
            (31, 33),
        ],
            self._split_these_minutes([10, 11, 12, 20, 31, 32, 33])
        )

    def test_that_it_blows_up_if_predictions_dont_increase(self):
        assert_raises(
            ValueError,
            lambda: self._split_these_minutes([5, 6, 7, 7, 8, 9])
        )

    def test_that_it_blows_up_if_predictions_decrease_in_time(self):
        assert_raises(
            ValueError,
            lambda: self._split_these_minutes([5, 6, 7, 6, 7, 8])
        )

    def test_that_it_handles_empty_predictions(self):
        assert_equal([], self._split_these_minutes([]))
