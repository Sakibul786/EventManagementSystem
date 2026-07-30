from django import forms
from .models import Category, Event, Participant


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

            # NEW IMAGE FIELD
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