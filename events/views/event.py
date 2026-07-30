from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

from events.models import Event, Category, Participant
from events.forms import EventForm


# -----------------------------
# Role Checking Functions
# -----------------------------

def is_admin_or_organizer(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Admin").exists()
        or user.groups.filter(name="Organizer").exists()
    )


# -----------------------------
# Event List
# -----------------------------

@login_required
def event_list(request):

    events = (
        Event.objects
        .select_related("category")
        .prefetch_related("participants")
    )

    categories = Category.objects.all()

    # Search
    search = request.GET.get("search", "")

    if search:
        events = events.filter(
            Q(name__icontains=search)
            | Q(location__icontains=search)
        )

    # Category Filter
    category = request.GET.get("category", "")

    if category:
        events = events.filter(category_id=category)

    # Date Filter
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    if start_date:
        events = events.filter(date__gte=start_date)

    if end_date:
        events = events.filter(date__lte=end_date)

    events = events.order_by("date", "time")

    paginator = Paginator(events, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "events": page_obj,
        "categories": categories,
        "search": search,
        "selected_category": category,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(
        request,
        "events/event/event_list.html",
        context,
    )


# -----------------------------
# Create Event
# -----------------------------

@login_required
@user_passes_test(is_admin_or_organizer)
def event_create(request):

    if request.method == "POST":

        form = EventForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event created successfully."
            )

            return redirect("event_list")

    else:

        form = EventForm()

    return render(
        request,
        "events/event/event_form.html",
        {
            "form": form,
        },
    )


# -----------------------------
# Update Event
# -----------------------------

@login_required
@user_passes_test(is_admin_or_organizer)
def event_update(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk,
    )

    if request.method == "POST":

        form = EventForm(
            request.POST,
            request.FILES,
            instance=event,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event updated successfully."
            )

            return redirect("event_list")

    else:

        form = EventForm(
            instance=event,
        )

    return render(
        request,
        "events/event/event_form.html",
        {
            "form": form,
        },
    )


# -----------------------------
# Delete Event
# -----------------------------

@login_required
@user_passes_test(is_admin_or_organizer)
def event_delete(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk,
    )

    if request.method == "POST":

        event.delete()

        messages.success(
            request,
            "Event deleted successfully."
        )

        return redirect("event_list")

    return render(
        request,
        "events/event/event_confirm_delete.html",
        {
            "event": event,
        },
    )


# -----------------------------
# Register Event
# -----------------------------

@login_required
def register_event(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk,
    )

    participant = get_object_or_404(
        Participant,
        user=request.user,
    )

    # Already registered
    if participant in event.participants.all():

        messages.warning(
            request,
            "You are already registered for this event."
        )

        return redirect("event_detail", pk=event.pk)

    # Event Full
    if event.is_full:

        messages.error(
            request,
            "Sorry! This event is already full."
        )

        return redirect("event_detail", pk=event.pk)

    # Register
    event.participants.add(participant)

    messages.success(
        request,
        "Successfully registered for the event."
    )

    return redirect("event_detail", pk=event.pk)


# -----------------------------
# Unregister Event
# -----------------------------

@login_required
def unregister_event(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk,
    )

    participant = get_object_or_404(
        Participant,
        user=request.user,
    )

    if participant in event.participants.all():

        event.participants.remove(participant)

        messages.success(
            request,
            "You have cancelled your registration."
        )

    else:

        messages.warning(
            request,
            "You are not registered for this event."
        )

    return redirect("event_detail", pk=event.pk)

# -----------------------------
# My Events
# -----------------------------

@login_required
def my_events(request):

    # Only Participants can access this page
    if not request.user.groups.filter(name="Participant").exists():

        messages.warning(
            request,
            "Only participants can view registered events."
        )

        return redirect("event_list")

    participant = get_object_or_404(
        Participant,
        user=request.user,
    )

    events = (
        participant.events
        .select_related("category")
        .order_by("date", "time")
    )

    return render(
        request,
        "events/event/my_events.html",
        {
            "events": events,
        },
    )

# -----------------------------
# Event Detail
# -----------------------------

@login_required
def event_detail(request, pk):

    event = get_object_or_404(
        Event.objects
        .select_related("category")
        .prefetch_related("participants"),
        pk=pk,
    )

    is_registered = False

    if hasattr(request.user, "participant_profile"):

        is_registered = event.participants.filter(
            pk=request.user.participant_profile.pk
        ).exists()

    context = {
        "event": event,
        "is_registered": is_registered,
    }

    return render(
        request,
        "events/event/event_detail.html",
        context,
    )