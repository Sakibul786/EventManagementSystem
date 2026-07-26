from django.shortcuts import render, redirect, get_object_or_404

from events.models import Participant
from events.forms import ParticipantForm
from django.contrib import messages


def participant_list(request):
    participants = Participant.objects.all()

    return render(
        request,
        "events/participant/participant_list.html",
        {"participants": participants},
    )


def participant_create(request):

    if request.method == "POST":
        form = ParticipantForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Participant created successfully.")
            return redirect("participant_list")

    else:
        form = ParticipantForm()

    return render(
        request,
        "events/participant/participant_form.html",
        {"form": form},
    )


def participant_update(request, pk):

    participant = get_object_or_404(Participant, pk=pk)

    if request.method == "POST":

        form = ParticipantForm(
            request.POST,
            instance=participant
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Participant updated successfully.")
            return redirect("participant_list")

    else:
        form = ParticipantForm(instance=participant)

    return render(
        request,
        "events/participant/participant_form.html",
        {"form": form},
    )


def participant_delete(request, pk):

    participant = get_object_or_404(Participant, pk=pk)

    if request.method == "POST":
        participant.delete()
        messages.success(request, "Participant deleted successfully.")
        return redirect("participant_list")

    return render(
        request,
        "events/participant/participant_confirm_delete.html",
        {"participant": participant},
    )