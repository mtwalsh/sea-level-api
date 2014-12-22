# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20140822_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='visible',
            field=models.BooleanField(default=True, help_text='Whether the location should be listed in the locations endpoint. Note that invisible locations can still be accessed through other endpoints if their slug is known.'),
            preserve_default=True,
        ),
    ]
