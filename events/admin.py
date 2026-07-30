from django.contrib import admin
from .models import Category, Event, Participant, Attendance


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("name", "email")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "date",
        "time",
        "location",
        "capacity",
        "participant_count",
    )
    list_filter = ("category", "date")
    search_fields = ("name", "location")
    filter_horizontal = ("participants",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "participant",
        "is_present",
        "marked_at",
    )
    list_filter = (
        "event",
        "is_present",
    )
    search_fields = (
        "participant__name",
        "participant__email",
        "event__name",
    )