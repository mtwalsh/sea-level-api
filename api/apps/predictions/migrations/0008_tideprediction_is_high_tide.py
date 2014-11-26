# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0007_auto_django_17rc3_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='tideprediction',
            name='is_high_tide',
            field=models.BooleanField(default=False, help_text='Does this tide prediction correspond to a high tide.'),
            preserve_default=True,
        ),
    ]
