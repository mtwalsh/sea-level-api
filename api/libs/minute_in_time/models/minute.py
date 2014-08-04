from __future__ import unicode_literals

import pytz

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Minute(models.Model):
    class Meta:
        app_label = 'minute_in_time'

    datetime = models.DateTimeField(unique=True)

    def save(self, *args, **kwargs):
        if self.datetime.tzinfo != pytz.UTC:
            raise ValueError("datetime must have pytz.UTC timezone.")
        self.datetime = self.datetime.replace(second=0, microsecond=0)
        super(Minute, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.datetime)
