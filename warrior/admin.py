from django.contrib import admin
from warrior.models import Warrior


@admin.register(Warrior)
class WarriorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
