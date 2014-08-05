from api.apps.observations.models import Observation
from api.libs.minute_in_time.models import Minute


def create_observation(location, when, measurement, is_interpolated):
    minute, _ = Minute.objects.get_or_create(datetime=when)
    obs, _ = Observation.objects.update_or_create(
        minute=minute,
        location=location,
        defaults={'sea_level': measurement, 'is_interpolated': is_interpolated}
    )
    return obs
