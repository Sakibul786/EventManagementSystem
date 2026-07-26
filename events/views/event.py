from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from events.models import Event, Category
from events.forms import EventForm
from django.contrib import messages
from django.core.paginator import Paginator


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
            Q(name__icontains=search) |
            Q(location__icontains=search)
        )

    # Category Filter
    category = request.GET.get("category", "")

    if category:
        events = events.filter(category_id=category)

    # Date Range Filter
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    if start_date:
        events = events.filter(date__gte=start_date)

    if end_date:
        events = events.filter(date__lte=end_date)
    # Order events
    events = events.order_by("date", "time")

    # Pagination
    paginator = Paginator(events, 5)  # Show 5 events per page

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


def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Event Created successfully.")
            return redirect("event_list")

    else:
        form = EventForm()

    return render(
        request,
        "events/event/event_form.html",
        {"form": form},
    )


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        form = EventForm(
            request.POST,
            instance=event,
        )

        if form.is_valid():
          form.save()
          messages.success(request, "Event Updated successfully.")
          return redirect("event_list")

    else:
        form = EventForm(instance=event)

    return render(
        request,
        "events/event/event_form.html",
        {"form": form},
    )


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event Deleted successfully.")
        return redirect("event_list")

    return render(
        request,
        "events/event/event_confirm_delete.html",
        {"event": event},
    )