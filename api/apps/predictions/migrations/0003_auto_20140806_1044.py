# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import F


def check_all_minutes_are_equal_to_datetimes(apps, schema_editor):
    Prediction = apps.get_model('predictions', 'Prediction')
    # db_alias = schema_editor.connection.alias
    num_bad_minutes = Prediction.objects.all().exclude(
        datetime=F('minute__datetime')).count()
    assert num_bad_minutes == 0, \
        "Not all Prediction.minute.datetime == Prediction.datetime"


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0002_prediction_minute'),
    ]

    operations = [
        migrations.RunPython(
            check_all_minutes_are_equal_to_datetimes
        ),
        migrations.AlterUniqueTogether(
            name='prediction',
            unique_together=set([('location', 'minute')]),
        ),
        migrations.RemoveField(
            model_name='prediction',
            name='datetime',
        ),
    ]
