from django.contrib import admin
from api.apps.surge_model_converter.models import ModelLocation


@admin.register(ModelLocation)
class ModelLocationAdmin(admin.ModelAdmin):
    list_display = ('surge_model_name', 'location')
