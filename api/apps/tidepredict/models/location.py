from django.db import models


class Location(models.Model):
    class Meta:
        app_label = 'tidepredict'

    slug = models.SlugField(max_length=100, unique=True)
