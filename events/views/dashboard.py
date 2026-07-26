from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count

from events.models import Event, Participant, Category


def dashboard(request):
    today = timezone.localdate()

    total_events = Event.objects.count()

    total_participants = Participant.objects.aggregate(
        total=Count("id")
    )["total"]

    total_categories = Category.objects.aggregate(
        total=Count("id")
    )["total"]

    upcoming_events = Event.objects.filter(
        date__gt=today
    ).count()

    past_events = Event.objects.filter(
        date__lt=today
    ).count()

    today_events = (
        Event.objects
        .select_related("category")
        .prefetch_related("participants")
        .filter(date=today)
    )

    context = {
        "total_events": total_events,
        "total_participants": total_participants,
        "total_categories": total_categories,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "today_events": today_events,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )
def dashboard_events(request):
    events = (
        Event.objects
        .select_related("category")
        .prefetch_related("participants")
        .order_by("date", "time")
    )

    return render(
        request,
        "all_events.html",
        {"events": events},
    )


def dashboard_categories(request):
    categories = Category.objects.order_by("name")

    return render(
        request,
        "all_categories.html",
        {"categories": categories},
    )


def dashboard_participants(request):
    participants = Participant.objects.order_by("name")

    return render(
        request,
        "all_participants.html",
        {"participants": participants},
    )


def dashboard_upcoming(request):
    today = timezone.localdate()

    events = (
        Event.objects
        .select_related("category")
        .prefetch_related("participants")
        .filter(date__gte=today)
        .order_by("date", "time")
    )

    return render(
        request,
        "upcoming_events.html",
        {"events": events},
    )


def dashboard_past(request):
    today = timezone.localdate()

    events = (
        Event.objects
        .select_related("category")
        .prefetch_related("participants")
        .filter(date__lt=today)
        .order_by("-date", "-time")
    )

    return render(
        request,
        "past_events.html",
        {"events": events},
    )