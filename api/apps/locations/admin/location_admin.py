from django.contrib import admin
from api.apps.locations.models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
