from django.contrib import admin

# Register your models here.
from .models import Solo


class SoloAdmin(admin.ModelAdmin):
    model = Solo
    list_display = ('track__album', 'name', 'get_duration')


admin.site.register(Solo, SoloAdmin)
