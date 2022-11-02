from django.contrib import admin

from main.models import Castle, ResourceBuildings, MilitaryBuildings, Buildings


@admin.register(Castle)
class CastleAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                )
            }
        ),
        (
            "Ресурсы",
            {
                "fields": (
                    "wood",
                    "stones",
                    "iron",
                    "food",
                )
            }
        ),
    )


@admin.register(ResourceBuildings)
class ResourceBuildingsAdmin(admin.ModelAdmin):
    pass


@admin.register(MilitaryBuildings)
class MilitaryBuildingsAdmin(admin.ModelAdmin):
    pass


@admin.register(Buildings)
class BuildingsAdmin(admin.ModelAdmin):
    pass
