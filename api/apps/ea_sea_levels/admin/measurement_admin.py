from django.contrib import admin
from api.apps.ea_sea_levels.models import Measurement


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('station', 'datetime', 'measurement')
