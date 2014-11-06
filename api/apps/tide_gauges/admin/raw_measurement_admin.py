from django.contrib import admin
from ..models import RawMeasurement


@admin.register(RawMeasurement)
class RawMeasurementAdmin(admin.ModelAdmin):
    _ALL_FIELDS = ('tide_gauge', 'datetime', 'height')

    list_display = _ALL_FIELDS
    readonly_fields = _ALL_FIELDS

    def has_add_permission(self, request):
        return False
