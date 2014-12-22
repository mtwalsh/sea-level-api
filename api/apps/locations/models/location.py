from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

from django.utils.encoding import python_2_unicode_compatible


STRICT_SLUG_VALIDATOR = RegexValidator(
    r'^' + settings.SLUG_REGEX + '$',
    'Only lowercase alphanumeric characters and hyphens are allowed.')


@python_2_unicode_compatible
class Location(models.Model):
    class Meta:
        app_label = 'locations'

    slug = models.SlugField(
        max_length=100,
        unique=True,
        validators=[STRICT_SLUG_VALIDATOR])

    name = models.CharField(max_length=100, blank=False, default="")

    visible = models.BooleanField(
        default=True,
        help_text='Whether the location should be listed in the locations '
                  'endpoint. Note that invisible locations can still be '
                  'accessed through other endpoints if their slug is known.')

    def __str__(self):
        return self.name
