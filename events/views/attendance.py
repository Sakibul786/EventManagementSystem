from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from events.models import Event, Attendance

from events.utils.pdf import generate_attendance_pdf
from events.utils.excel import generate_attendance_excel


def is_admin_or_organizer(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Admin").exists()
        or user.groups.filter(name="Organizer").exists()
    )


@login_required
@user_passes_test(is_admin_or_organizer)
def attendance_list(request, event_id):

    event = get_object_or_404(
        Event.objects.prefetch_related("participants"),
        pk=event_id,
    )

    attendance_records = []

    for participant in event.participants.all():

        attendance, created = Attendance.objects.get_or_create(
            event=event,
            participant=participant,
        )

        attendance_records.append(attendance)

    total_registered = len(attendance_records)

    total_present = sum(
        1 for record in attendance_records if record.is_present
    )

    total_absent = total_registered - total_present

    attendance_percentage = (
        round((total_present / total_registered) * 100, 1)
        if total_registered > 0
        else 0
    )

    return render(
        request,
        "events/attendance/attendance_list.html",
        {
            "event": event,
            "attendance_records": attendance_records,
            "total_registered": total_registered,
            "total_present": total_present,
            "total_absent": total_absent,
            "attendance_percentage": attendance_percentage,
        },
    )


@login_required
@user_passes_test(is_admin_or_organizer)
def toggle_attendance(request, attendance_id):

    attendance = get_object_or_404(
        Attendance,
        pk=attendance_id,
    )

    attendance.is_present = not attendance.is_present
    attendance.save()

    messages.success(
        request,
        "Attendance updated successfully.",
    )

    return redirect(
        "attendance_list",
        event_id=attendance.event.id,
    )


@login_required
@user_passes_test(is_admin_or_organizer)
def export_attendance_pdf(request, event_id):

    event = get_object_or_404(
        Event.objects.prefetch_related("participants"),
        pk=event_id,
    )

    return generate_attendance_pdf(event)


@login_required
@user_passes_test(is_admin_or_organizer)
def export_attendance_excel(request, event_id):

    event = get_object_or_404(
        Event.objects.prefetch_related("participants"),
        pk=event_id,
    )

    return generate_attendance_excel(event)