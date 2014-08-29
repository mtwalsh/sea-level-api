from django.core.validators import RegexValidator
from django.db import models

from api.apps.locations.models import Location

from django.utils.encoding import python_2_unicode_compatible

MODEL_NAME_VALIDATOR = RegexValidator(
    r'^[A-Z]{4}$',
    'Only four-letter uppercase names are allowed.')


@python_2_unicode_compatible
class ModelLocation(models.Model):
    class Meta:
        app_label = 'surge_model_converter'

    location = models.ForeignKey(
        Location,
        help_text='The location to which this surge-model location relates')

    surge_model_name = models.CharField(
        max_length=4,
        help_text='The 4-character code used by the surge model to identify '
                  'this location.',
        validators=[MODEL_NAME_VALIDATOR])

    def __str__(self):
        return self.surge_model_name
