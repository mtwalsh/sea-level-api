from django.contrib import admin
from api.apps.status.models import LocationStatusConfig


@admin.register(LocationStatusConfig)
class LocationStatusConfigAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'disabled_alerts')
