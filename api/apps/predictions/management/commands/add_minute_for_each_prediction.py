from django_docopt_command import DocOptCommand
from api.apps.predictions.models import Prediction
from api.libs.minute_in_time.models import Minute


class Command(DocOptCommand):
    docs = "Usage: add_minute_for_each_prediction"

    def handle_docopt(self, arguments):
        predictions = Prediction.objects.filter(minute=None)

        create_and_attach_minutes(predictions, self.stdout)


def create_and_attach_minutes(predictions, stdout=None):
    count = 0
    num_predictions = predictions.count()
    for prediction in predictions:
        count += 1

        if 0 == (count % 1000):
            if stdout is not None:
                stdout.write('{} / {}'.format(count, num_predictions))

        minute, _ = Minute.objects.get_or_create(datetime=prediction.datetime)
        prediction.minute = minute
        prediction.save()
