# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0002_auto_20140620_1129'),
    ]

    operations = [
        migrations.RenameField('prediction', 'tide_height', 'tide_level'),
    ]
