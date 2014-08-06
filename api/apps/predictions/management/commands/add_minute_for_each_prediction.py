import time

from django.core.management.base import BaseCommand
from django.db import transaction

from api.apps.predictions.models import Prediction
from api.libs.minute_in_time.models import Minute


class Command(BaseCommand):
    """
    Throw-away command: in each Prediction, add a foreign key to a Minute
    model matching the Prediction's datetime.
    """

    def handle(self, *args, **options):
        datetimes_to_be_created = self.get_missing_minute_datetimes()
        self.bulk_create_minutes(datetimes_to_be_created)

        minute_hash = self.get_minutes_by_datetime()

        predictions = self.get_predictions_without_minute()
        self.attach_minutes(predictions, minute_hash)

    def get_missing_minute_datetimes(self):
        self.stdout.write("Finding missing Minute objects")
        return (set(p.datetime for p in Prediction.objects.all())
                - set(m.datetime for m in Minute.objects.all()))

    def bulk_create_minutes(self, datetimes):
        self.stdout.write("Bulk creating {} minutes".format(len(datetimes)))
        Minute.objects.bulk_create(Minute(datetime=dt) for dt in datetimes)

    def get_predictions_without_minute(self):
        self.stdout.write("Getting predictions without minutes")
        return Prediction.objects.filter(minute=None)

    def get_minutes_by_datetime(self):
        self.stdout.write("Generating datetime->Minute hash")
        return {minute.datetime: minute for minute in Minute.objects.all()}

    def attach_minutes(self, predictions, minute_hash):
        self.stdout.write("Attaching Minutes to Predictions")
        transaction.set_autocommit(False)
        count = 0
        num_predictions = predictions.count()
        for prediction in predictions:
            count += 1

            if 0 == (count % 1000):
                self.stdout.write('{} / {}'.format(count, num_predictions))
                transaction.commit()
                time.sleep(0.25)

            prediction.minute = minute_hash[prediction.datetime]
            prediction.save()
