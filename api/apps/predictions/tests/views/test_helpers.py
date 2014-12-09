import datetime
import pytz

from nose.tools import assert_equal, assert_raises

from django.test import TestCase

from api.apps.predictions.views.helpers import (
    split_predictions_into_tide_windows)

BASE_DATETIME = datetime.datetime(2013, 1, 1, 10, 0, 0, tzinfo=pytz.UTC)


class FakeTideWindow(object):
    def __init__(self, start_minute, end_minute, high_tide_minute):
        self.start_minute = start_minute
        self.end_minute = end_minute
        self.high_tide_minute = high_tide_minute

    @classmethod
    def from_real_window(cls, real_window):
        return FakeTideWindow(
            cls._to_mins(real_window.start_prediction),
            cls._to_mins(real_window.end_prediction),
            cls._to_mins(real_window.high_tide_prediction))

    @classmethod
    def _to_mins(cls, prediction):
        dt = prediction.minute.datetime
        return int((dt - BASE_DATETIME).total_seconds() / 60)

    def __eq__(self, other):
        return (self.start_minute == other.start_minute
                and self.end_minute == other.end_minute
                and self.high_tide_minute == other.high_tide_minute)

    def __repr__(self):
        return 'FakeTideWindow(start={}, end={}, high={})'.format(
            self.start_minute, self.end_minute, self.high_tide_minute)


class FakeMinute(object):
    def __init__(self, datetime):
        self.datetime = datetime


class FakePrediction(object):
    """
    Lightweight pretend Prediction object for testing calculations without
    hitting the database.
    """
    def __init__(self, minute, is_high_tide=False):
        self.minute = FakeMinute(BASE_DATETIME.replace(minute=minute))
        self.is_high_tide = is_high_tide


class TestSplitPrediction(TestCase):
    def _split_these_predictions(self, predictions):
        return [FakeTideWindow.from_real_window(window)
                for window in split_predictions_into_tide_windows(predictions)]

    def test_split_prediction_windows_splits_single_window(self):
        assert_equal([
            FakeTideWindow(2, 4, 3),
        ],
            self._split_these_predictions([
                FakePrediction(2),
                FakePrediction(3, True),
                FakePrediction(4)])
        )

    def test_that_it_splits_window_with_only_two_predictions(self):
        assert_equal([
            FakeTideWindow(2, 3, 3),
        ],
            self._split_these_predictions([
                FakePrediction(2),
                FakePrediction(3, True)])
        )

    def test_that_it_splits_multiple_windows_correctly(self):
        assert_equal([
            FakeTideWindow(2, 4, 3),
            FakeTideWindow(10, 12, 11),
            FakeTideWindow(25, 26, 26),
        ],
            self._split_these_predictions([
                FakePrediction(2),
                FakePrediction(3, True),
                FakePrediction(4),
                FakePrediction(10),
                FakePrediction(11, True),
                FakePrediction(12),
                FakePrediction(25),
                FakePrediction(26, True)])
        )

    def test_that_it_ignores_single_predictions_at_start(self):
        assert_equal([
            FakeTideWindow(10, 13, 11),
        ],
            self._split_these_predictions([
                FakePrediction(3),
                FakePrediction(10),
                FakePrediction(11, True),
                FakePrediction(12),
                FakePrediction(13)])
        )

    def test_that_it_ignores_single_predictions_at_end(self):
        assert_equal([
            FakeTideWindow(10, 13, 12),
        ],
            self._split_these_predictions([
                FakePrediction(10),
                FakePrediction(11),
                FakePrediction(12, True),
                FakePrediction(13),
                FakePrediction(34)])
        )

    def test_that_it_ignores_single_predictions_in_middle(self):
        assert_equal([
            FakeTideWindow(10, 12, 11),
            FakeTideWindow(31, 33, 32),
        ],
            self._split_these_predictions([
                FakePrediction(10),
                FakePrediction(11, True),
                FakePrediction(12),
                FakePrediction(20),
                FakePrediction(31),
                FakePrediction(32, True),
                FakePrediction(33)])
        )

    def test_that_it_blows_up_if_predictions_dont_increase(self):
        assert_raises(
            ValueError,
            lambda: self._split_these_predictions([
                FakePrediction(5),
                FakePrediction(6),
                FakePrediction(7, True),
                FakePrediction(7),
                FakePrediction(8),
                FakePrediction(9)])
        )

    def test_that_it_blows_up_if_predictions_decrease_in_time(self):
        assert_raises(
            ValueError,
            lambda: self._split_these_predictions([
                FakePrediction(5),
                FakePrediction(6),
                FakePrediction(7, True),
                FakePrediction(6),
                FakePrediction(7),
                FakePrediction(8)])
        )

    def test_that_it_handles_empty_predictions(self):
        assert_equal([], self._split_these_predictions([]))

    def test_that_multiple_high_tides_make_repeating_tide_windows(self):
        assert_equal([
            FakeTideWindow(10, 16, 11),
            FakeTideWindow(10, 16, 14),
        ],
            self._split_these_predictions([
                FakePrediction(10),
                FakePrediction(11, True),
                FakePrediction(12),
                FakePrediction(13),
                FakePrediction(14, True),
                FakePrediction(15),
                FakePrediction(16)])
        )
