from ..models import TidePrediction
from api.libs.minute_in_time.models import Minute


def create_tide_prediction(location, datetime, tide_level, is_high_tide=False):
    minute, _ = Minute.objects.get_or_create(datetime=datetime)
    prediction, _ = TidePrediction.objects.update_or_create(
        minute=minute,
        location=location,
        defaults={'tide_level': tide_level,
                  'is_high_tide': is_high_tide}
    )
    return prediction
