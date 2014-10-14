import datetime

from enum import Enum

import pytz

from .models import LocationStatusConfig

AlertType = Enum('AlertType',
                 'tide_predictions surge_predictions observations')


def disable_alert_until(location, alert_type, dt):
    now = datetime.datetime.now(pytz.UTC)
    assert now <= dt <= (now + datetime.timedelta(days=60)), (
        '{}: Datetime must be between now and 60 days '
        'from now. See `enable_alert` if you just want to '
        'enable the alert type.'.format(dt))

    config = _get_status_configuration(location)
    attr_name = _disabled_until_attr_name(alert_type)

    setattr(config, attr_name, dt)
    config.save()


def enable_alert(location, alert_type):
    config = _get_status_configuration(location)
    attr_name = _disabled_until_attr_name(alert_type)
    setattr(config, attr_name, None)
    config.save()


def enable_all_alerts(location):
    for alert_type in AlertType:
        enable_alert(location, alert_type)


def is_alert_enabled(location, alert_type):
    config = _get_status_configuration(location)

    attr_name = _disabled_until_attr_name(alert_type)
    disabled_until = getattr(config, attr_name)

    if disabled_until is None:
        return True  # no disabled_until => enabled
    else:
        now = datetime.datetime.now(pytz.UTC)
        expired = (now >= disabled_until)
        if expired:  # replace expired datetime with None
            enable_alert(location, alert_type)
        return expired


def alerts_enabled(location):
    return set([a for a in AlertType if is_alert_enabled(location, a)])


def alerts_disabled(location):
    return set(AlertType) - alerts_enabled(location)


def _disabled_until_attr_name(alert_type):
    return '{alert_type}_alerts_disabled_until'.format(
        alert_type=alert_type.name)


def _get_status_configuration(location):
    (ob, _) = LocationStatusConfig.objects.get_or_create(location=location)
    return ob
