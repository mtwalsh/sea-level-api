from django.contrib import admin
from api.apps.sea_levels.models import CombinedPredictionObservation


@admin.register(CombinedPredictionObservation)
class CombinedPredictionObservationAdmin(admin.ModelAdmin):
    readonly_fields = ('datetime', 'predicted_tide_level', 'location',
                       'observed_sea_level', 'derived_surge_level')
    list_display = ('__str__', 'datetime', 'location', 'predicted_tide_level',
                    'observed_sea_level', 'derived_surge_level')

    def has_add_permission(self, request):
        return False
