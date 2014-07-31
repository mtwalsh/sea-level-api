from django.contrib import admin
from api.apps.ea_sea_levels.models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('station_name', 'station_id')
