from django.contrib import admin
from ..models import TideGauge


@admin.register(TideGauge)
class TideGaugeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'comment')
