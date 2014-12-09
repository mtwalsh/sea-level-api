import datetime

import logging
logger = logging.getLogger(__name__)

from collections import namedtuple
from itertools import tee

try:
    from itertools import izip as zip  # On 2, replace zip with izip
except ImportError:
    pass  # Python 3 has zip already

from api.libs.param_parsers import parse_location, parse_time_range

from ..models import TidePrediction


TimeRange = namedtuple('TimeRange', 'start,end')
ONE_DAY = datetime.timedelta(hours=24)
ONE_MIN = datetime.timedelta(seconds=60)


def parse_and_get_queryset(location_slug, start_param, end_param):
    location = parse_location(location_slug)
    time_range = parse_time_range(start_param, end_param)
    return get_queryset(location, time_range)


def get_queryset(location, time_range):
    queryset = TidePrediction.objects.filter(
        location=location,
        minute__datetime__gte=time_range.start,
        minute__datetime__lt=time_range.end).select_related('minute')

    return queryset.order_by('minute__datetime')


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def split_predictions_into_tide_windows(predictions):
    if not predictions:
        return

    current_tide_window = TideWindow()

    for p0, p1 in pairwise(predictions):
        current_tide_window.add_prediction(p0)

        time_interval = p1.minute.datetime - p0.minute.datetime

        if time_interval > ONE_MIN:  # gap: split
            for tide_window in current_tide_window.spawn_for_each_high_tide():
                yield tide_window

            current_tide_window = TideWindow()

        elif time_interval <= datetime.timedelta(0):
            raise ValueError('Predictions must be ascending')

    current_tide_window.add_prediction(p1)
    for tide_window in current_tide_window.spawn_for_each_high_tide():
        yield tide_window


class TideWindow(object):
    def __init__(self):
        self.start_prediction = None
        self.end_prediction = None
        self.high_tide_predictions = []

    def validate(self):
        if not self.high_tide_predictions:
            logger.info('TideWindow invalid: no high tide predictions')
            return False

        if self.start_prediction is None:
            logger.info('TideWindow invalid: no start prediction')
            return False

        if self.end_prediction is None:
            logger.info('TideWindow invalid: no end prediction')
            return False

        if (self.high_tide_prediction.minute.datetime
                < self.start_prediction.minute.datetime):
            logger.info('TideWindow invalid: high tide before start')
            return False

        if (self.high_tide_prediction.minute.datetime
                > self.end_prediction.minute.datetime):
            logger.info('TideWindow invalid: high tide after end')
            return False

        return True

    def spawn_for_each_high_tide(self):
        for high_tide_prediction in self.high_tide_predictions:
            t = TideWindow()
            t.start_prediction = self.start_prediction
            t.end_prediction = self.end_prediction
            t.high_tide_prediction = high_tide_prediction
            yield t

    def add_prediction(self, prediction):
        if self.start_prediction is None:
            self.start_prediction = prediction
        else:
            self.end_prediction = prediction

        if prediction.is_high_tide:
            self.high_tide_predictions.append(prediction)

    @property
    def high_tide_prediction(self):
        assert len(self.high_tide_predictions) == 1
        return self.high_tide_predictions[0]

    @high_tide_prediction.setter
    def high_tide_prediction(self, prediction):
        self.high_tide_predictions = [prediction]

    def is_inside_time_range(self, time_range):
        """
        Return True if the self is fully or partially inside the given time
        range
                          start          end
                            |             |
                  <--F--> <--T--> <-T->  <--T-->  <--F-->

        where first <------> last
        """
        return (self.start_prediction.minute.datetime <= time_range.end
                and self.end_prediction.minute.datetime >= time_range.start)

    def truncate_end(self, to_datetime):
        self.end_prediction = TidePrediction.objects.get(
            minute__datetime=to_datetime)

    def truncate_start(self, to_datetime):
        self.start_prediction = TidePrediction.objects.get(
            minute__datetime=to_datetime)

    def extends_after(self, when):
        return (self.end_prediction.minute.datetime
                >= when - datetime.timedelta(minutes=1))  # TODO ratty?

    def extends_before(self, when):
        return self.start_prediction.minute.datetime <= when
