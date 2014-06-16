# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='slug',
            field=models.SlugField(unique=True, max_length=100, validators=[django.core.validators.RegexValidator(b'^[0-9a-z-]+$', b'Only lowercase alphanumeric characters and hyphens are allowed.')]),
        ),
    ]
