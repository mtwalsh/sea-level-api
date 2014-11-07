from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

from django.utils.encoding import python_2_unicode_compatible


STRICT_SLUG_VALIDATOR = RegexValidator(
    r'^' + settings.SLUG_REGEX + '$',
    'Only lowercase alphanumeric characters and hyphens are allowed.')


@python_2_unicode_compatible
class TideGauge(models.Model):
    class Meta:
        app_label = 'tide_gauges'

    slug = models.SlugField(
        max_length=100,
        unique=True,
        validators=[STRICT_SLUG_VALIDATOR])

    comment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.slug
