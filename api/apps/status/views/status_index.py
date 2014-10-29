import datetime
import pytz

from django.views.generic import View
from django.shortcuts import render

from collections import namedtuple

from api.apps.locations.models import Location
from api.apps.predictions.models import TidePrediction, SurgePrediction
from api.apps.observations.models import Observation

from ..alert_manager import AlertType, is_alert_enabled


LocationStatus = namedtuple('LocationStatus', 'name,checks')
Check = namedtuple('Check', 'name,status_text,status_class')


class StatusIndex(View):
    def get(self, request, *args, **kwargs):

        all_ok, location_statuses = get_checks_by_location()
        status_code = 200 if all_ok else 500
        summary_status = 'OK' if all_ok else 'ERROR'

        return render(
            request,
            'status/status_index.html',
            {'location_statuses': location_statuses,
             'summary_status': summary_status},
            status=status_code)


def get_checks_by_location():
    statuses = []
    all_ok = True

    for location in Location.objects.all():
        ok, location_status = get_location_status(location)
        all_ok = all_ok and ok
        statuses.append(location_status)

    return all_ok, statuses


def get_location_status(location):
    checks_to_run = [
        ('Tide predictions', check_tide_predictions),
        ('Surge predictions', check_surge_predictions),
        ('Observations', check_observations),
    ]
    all_ok = True
    checks = []
    for name, function in checks_to_run:
        ok, text = function(location)
        all_ok = all_ok and ok
        checks.append(Check(
            name=name,
            status_text=text,
            status_class='success' if ok else 'danger'))

    return all_ok, LocationStatus(name=location.name, checks=checks)


def check_tide_predictions(location):
    if not is_alert_enabled(location, AlertType.tide_predictions):
        return (True, 'OK (alert disabled)')

    one_month_away = (datetime.datetime.now(pytz.UTC)
                      + datetime.timedelta(days=30))

    ok = TidePrediction.objects.filter(
        location=location,
        minute__datetime__gte=one_month_away).exists()

    if ok:
        return (True, 'OK')
    else:
        return (False, '< 30 days left')


def check_surge_predictions(location):
    """
    Test that we have a surge prediction for every minute in the next 36 hours.
    """
    if not is_alert_enabled(location, AlertType.surge_predictions):
        return (True, 'OK (alert disabled)')

    now = datetime.datetime.now(pytz.UTC)
    thirty_seven_hours_away = now + datetime.timedelta(hours=36)

    count = SurgePrediction.objects.filter(
        location=location,
        minute__datetime__gte=now,
        minute__datetime__lt=thirty_seven_hours_away).count()
    ok = (36 * 60) == count

    if ok:
        return (True, 'OK')
    else:
        return (False,
                'Missing data for next 36 hours: {} vs 2160'.format(count))


def check_observations(location):
    if not is_alert_enabled(location, AlertType.observations):
        return (True, 'OK (alert disabled)')

    one_hour_ago = (datetime.datetime.now(pytz.UTC)
                    - datetime.timedelta(minutes=60))

    ok = Observation.objects.filter(
        location=location,
        minute__datetime__gte=one_hour_ago).exists()

    if ok:
        return (True, 'OK')
    else:
        return (False, '> 1 hour old')
