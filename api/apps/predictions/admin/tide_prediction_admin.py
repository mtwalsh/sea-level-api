from django.contrib import admin
from api.apps.predictions.models import TidePrediction


@admin.register(TidePrediction)
class TidePredictionAdmin(admin.ModelAdmin):
    readonly_fields = ('tide_level', 'minute', 'location')

    def has_add_permission(self, request):
        return False
