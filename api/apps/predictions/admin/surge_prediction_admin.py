from django.contrib import admin
from api.apps.predictions.models import SurgePrediction


@admin.register(SurgePrediction)
class SurgePredictionAdmin(admin.ModelAdmin):
    readonly_fields = ('surge_level', 'minute', 'location')

    def has_add_permission(self, request):
        return False
