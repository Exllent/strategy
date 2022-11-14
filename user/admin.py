from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import CustomUser, Army


@admin.register(Army)
class ArmyAdmin(admin.ModelAdmin):
    pass


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('login', 'is_staff', 'is_active',)
    list_filter = ('login', 'is_staff', 'is_active',)
    search_fields = ('login',)
    ordering = ('login',)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "login",
                    "password"
                )
            }
        ),
        (
            "Персональная информация",
            {
                "fields": (
                    "nickname",
                    "slug",
                    "email",)
            }
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Важные даты",
            {
                "fields": (
                    "last_login",
                    "date_joined"
                )
            }
        ),
        (
            "Настройки игрока", {
                "fields": (
                    "silver_money",
                    "gold_money",
                    "army",
                    "race",
                    "castle"
                )
            }
        )
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("login", "slug", "password1", "password2",
                           "silver_money", "gold_money", "army", "race",),
            },
        ),
    )
    prepopulated_fields = {"slug": ("nickname",)}


admin.site.register(CustomUser, CustomUserAdmin)
