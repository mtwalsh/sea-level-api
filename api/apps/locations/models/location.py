from django.db import models
from django.core.validators import RegexValidator

STRICT_SLUG_VALIDATOR = RegexValidator(
    r'^[0-9a-z-]+$',
    'Only lowercase alphanumeric characters and hyphens are allowed.')


class Location(models.Model):
    class Meta:
        app_label = 'locations'

    slug = models.SlugField(
        max_length=100,
        unique=True,
        validators=[STRICT_SLUG_VALIDATOR])

    name = models.CharField(max_length=100, blank=False, default="")
