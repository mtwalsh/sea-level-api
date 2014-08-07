from django.contrib import admin
from api.apps.predictions.models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    readonly_fields = ('tide_level', 'minute', 'location')

    def has_add_permission(self, request):
        return False
