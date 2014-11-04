# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surge_model_converter', '0002_load_LVPL_location_20140828_1337'),
    ]

    operations = [
        migrations.DeleteModel('ModelLocation')
    ]
