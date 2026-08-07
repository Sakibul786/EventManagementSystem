from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Category,
    Event,
    Participant,
    OfflineAttendance,
)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = "__all__"

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2",
                    "rows": 4,
                }
            ),

        }


class ParticipantForm(forms.ModelForm):

    class Meta:
        model = Participant
        fields = "__all__"

        widgets = {

            "user": forms.Select(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2"
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2"
                }
            ),

            "profile_image": forms.ClearableFileInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2 bg-white"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2"
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2"
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2",
                    "rows": 3,
                }
            ),

        }

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = "__all__"

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2",
                    "rows": 4,
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2",
                }
            ),

            "time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2"
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2 bg-white"
                }
            ),

            "capacity": forms.NumberInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2",
                    "min": 1,
                    "placeholder": "Maximum participants",
                }
            ),

            "offline_participants": forms.NumberInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2",
                    "min": 0,
                    "placeholder": "Offline Participants",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2"
                }
            ),

            "participants": forms.SelectMultiple(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2 h-40"
                }
            ),

        }

    def clean(self):

        cleaned_data = super().clean()

        capacity = cleaned_data.get("capacity") or 0
        offline = cleaned_data.get("offline_participants") or 0
        participants = cleaned_data.get("participants")

        online = participants.count() if participants else 0

        if offline > capacity:

            self.add_error(
                "offline_participants",
                "Offline participants cannot be greater than the event capacity."
            )

        if online + offline > capacity:

            self.add_error(
                "participants",
                f"Total participants ({online + offline}) cannot exceed the event capacity ({capacity})."
            )

        return cleaned_data
    
class OfflineAttendanceForm(forms.ModelForm):

    class Meta:
        model = OfflineAttendance
        fields = [
            "present",
        ]

        widgets = {

            "present": forms.NumberInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-4 py-2",
                    "min": 0,
                    "placeholder": "Offline Present",
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        self.event = kwargs.pop("event", None)

        super().__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super().clean()

        present = cleaned_data.get("present") or 0

        if self.event:

            offline_registered = self.event.offline_participants

            if present > offline_registered:

                self.add_error(
                    "present",
                    "Offline present cannot exceed offline participants."
                )

        return cleaned_data