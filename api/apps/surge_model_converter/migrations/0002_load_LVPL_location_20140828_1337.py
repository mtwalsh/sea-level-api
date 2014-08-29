# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist


def create_liverpool_mapping(apps, schema_editor):
    Location = apps.get_model('locations', 'Location')
    ModelLocation = apps.get_model('surge_model_converter', 'ModelLocation')

    if 0 == ModelLocation.objects.all().count():
        try:
            location = Location.objects.get(slug='liverpool-gladstone-dock')
        except ObjectDoesNotExist:
            pass
        else:
            ModelLocation.objects.create(
                location=location,
                surge_model_name='LVPL')


class Migration(migrations.Migration):

    dependencies = [
        ('surge_model_converter', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_liverpool_mapping),
    ]
