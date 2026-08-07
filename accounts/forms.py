from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from events.models import Participant


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "w-full border rounded-lg px-4 py-2",
                "placeholder": "First Name",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "w-full border rounded-lg px-4 py-2",
                "placeholder": "Last Name",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full border rounded-lg px-4 py-2",
                "placeholder": "Email",
            }
        ),
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full border rounded-lg px-4 py-2",
                "placeholder": "Username",
            }
        ),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border rounded-lg px-4 py-2",
                "placeholder": "Password",
            }
        ),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border rounded-lg px-4 py-2",
                "placeholder": "Confirm Password",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):

        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_username(self):

        username = self.cleaned_data["username"].strip()

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError(
                "This username is already taken."
            )

        return username

class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=100,
    )

    last_name = forms.CharField(
        max_length=100,
    )

    email = forms.EmailField()

    class Meta:
        model = Participant
        fields = [
            "profile_image",
            "phone",
            "address",
            "bio",
        ]

        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "w-full border rounded-lg px-4 py-2",
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": "w-full border rounded-lg px-4 py-2",
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "w-full border rounded-lg px-4 py-2",
                }
            ),
        }    