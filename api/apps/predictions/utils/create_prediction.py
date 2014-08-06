from ..models import Prediction
from api.libs.minute_in_time.models import Minute


def create_prediction(location, datetime, tide_level):
    minute, _ = Minute.objects.get_or_create(datetime=datetime)
    prediction, _ = Prediction.objects.update_or_create(
        minute=minute,
        location=location,
        defaults={'tide_level': tide_level}
    )
    return prediction
