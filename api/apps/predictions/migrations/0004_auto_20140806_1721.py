# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0003_auto_20140806_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='minute',
            field=models.ForeignKey(to='minute_in_time.Minute'),
        ),
    ]
