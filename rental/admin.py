from django.contrib import admin

from .models import Aircraft, Assembly, Part, Personnel, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ("user_email", "team")

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "User Email"


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("part_type", "aircraft", "team", "stock")
    list_filter = ("part_type", "aircraft", "team")


@admin.register(Assembly)
class AssemblyAdmin(admin.ModelAdmin):
    list_display = ("aircraft", "assembled_at")
