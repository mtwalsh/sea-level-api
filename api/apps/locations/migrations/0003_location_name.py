# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20140616_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='name',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
    ]
