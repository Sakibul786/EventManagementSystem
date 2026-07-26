from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # Dashboard
    # ==========================

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "dashboard/events/",
        views.dashboard_events,
        name="dashboard_events",
    ),

    path(
        "dashboard/categories/",
        views.dashboard_categories,
        name="dashboard_categories",
    ),

    path(
        "dashboard/participants/",
        views.dashboard_participants,
        name="dashboard_participants",
    ),

    path(
        "dashboard/upcoming/",
        views.dashboard_upcoming,
        name="dashboard_upcoming",
    ),

    path(
        "dashboard/past/",
        views.dashboard_past,
        name="dashboard_past",
    ),

    # ==========================
    # Category
    # ==========================

    path(
        "categories/",
        views.category_list,
        name="category_list",
    ),

    path(
        "categories/add/",
        views.category_create,
        name="category_create",
    ),

    path(
        "categories/<int:pk>/edit/",
        views.category_update,
        name="category_update",
    ),

    path(
        "categories/<int:pk>/delete/",
        views.category_delete,
        name="category_delete",
    ),

    # ==========================
    # Participant
    # ==========================

    path(
        "participants/",
        views.participant_list,
        name="participant_list",
    ),

    path(
        "participants/add/",
        views.participant_create,
        name="participant_create",
    ),

    path(
        "participants/<int:pk>/edit/",
        views.participant_update,
        name="participant_update",
    ),

    path(
        "participants/<int:pk>/delete/",
        views.participant_delete,
        name="participant_delete",
    ),

    # ==========================
    # Event
    # ==========================

    path(
        "events/",
        views.event_list,
        name="event_list",
    ),

    path(
        "events/add/",
        views.event_create,
        name="event_create",
    ),

    path(
        "events/<int:pk>/edit/",
        views.event_update,
        name="event_update",
    ),

    path(
        "events/<int:pk>/delete/",
        views.event_delete,
        name="event_delete",
    ),
]