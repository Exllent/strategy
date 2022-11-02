from django.contrib import admin

from race.models import Race


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    pass
