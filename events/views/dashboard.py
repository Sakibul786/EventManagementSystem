from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test

from events.models import Event, Participant, Category
from django.db.models import Count, Q


# ==========================================
# Permission Functions
# ==========================================

def is_admin(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Admin").exists()
    )


def is_admin_or_organizer(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Admin").exists()
        or user.groups.filter(name="Organizer").exists()
    )


# ==========================================
# Dashboard (All Logged-in Users)
# ==========================================

@login_required
def dashboard(request):

    now = timezone.localtime()
    today = now.date()

    total_events = Event.objects.count()

    total_participants = Participant.objects.aggregate(
        total=Count("id")
    )["total"]

    total_categories = Category.objects.aggregate(
        total=Count("id")
    )["total"]

    upcoming_events = Event.objects.filter(
        Q(date__gt=today) |
        Q(date=today, time__gt=now.time())
    ).count()

    past_events = Event.objects.filter(
        Q(date__lt=today) |
        Q(date=today, time__lt=now.time())
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


# ==========================================
# All Events
# ==========================================

@login_required
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
        {
            "events": events,
        },
    )


# ==========================================
# Categories (Admin + Organizer)
# ==========================================

@login_required
@user_passes_test(is_admin_or_organizer)
def dashboard_categories(request):

    categories = Category.objects.order_by("name")

    return render(
        request,
        "all_categories.html",
        {
            "categories": categories,
        },
    )


# ==========================================
# Participants (Admin + Organizer)
# ==========================================

@login_required
@user_passes_test(is_admin_or_organizer)
def dashboard_participants(request):

    participants = Participant.objects.order_by("name")

    return render(
        request,
        "all_participants.html",
        {
            "participants": participants,
        },
    )


# ==========================================
# Upcoming Events
# ==========================================

@login_required
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
        {
            "events": events,
        },
    )


# ==========================================
# Past Events
# ==========================================

@login_required
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
        {
            "events": events,
        },
    )