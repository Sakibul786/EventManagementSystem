from django.contrib import admin
from .models import Category, Event, Participant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("name", "email")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "date", "time", "location")
    list_filter = ("category", "date")
    search_fields = ("name", "location")
    filter_horizontal = ("participants",)