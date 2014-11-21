from django.contrib import admin
from ..models import TideGaugeLocationLink


@admin.register(TideGaugeLocationLink)
class TideGaugeLocationLinkAdmin(admin.ModelAdmin):
    pass
