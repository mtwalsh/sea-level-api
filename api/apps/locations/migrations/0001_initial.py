# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100, validators=[django.core.validators.RegexValidator('^[0-9a-z-]+$', 'Only lowercase alphanumeric characters and hyphens are allowed.')])),
                ('name', models.CharField(default='', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
