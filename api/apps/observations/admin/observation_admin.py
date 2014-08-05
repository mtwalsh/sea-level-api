from django.contrib import admin
from api.apps.observations.models import Observation


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'minute', 'location')
