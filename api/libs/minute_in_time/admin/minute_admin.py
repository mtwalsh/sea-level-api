from django.contrib import admin
from api.libs.minute_in_time.models import Minute


@admin.register(Minute)
class MinuteAdmin(admin.ModelAdmin):
    pass
