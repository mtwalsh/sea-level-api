from ..models import SurgePrediction
from api.libs.minute_in_time.models import Minute


def create_surge_prediction(location, datetime, surge_level):
    minute, _ = Minute.objects.get_or_create(datetime=datetime)
    prediction, _ = SurgePrediction.objects.update_or_create(
        minute=minute,
        location=location,
        defaults={'surge_level': surge_level}
    )
    return prediction
