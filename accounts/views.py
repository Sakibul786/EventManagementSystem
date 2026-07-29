from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group

from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from .forms import SignUpForm
from .tokens import account_activation_token


def signup(request):

    if request.method == "POST":

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # User cannot login until email is verified
            user.is_active = False
            user.save()

            # Add user to Participant group
            participant_group, created = Group.objects.get_or_create(
                name="Participant"
            )
            user.groups.add(participant_group)

            current_site = get_current_site(request)

            mail_subject = "Activate your Event Management System account"

            message = render_to_string(
                "accounts/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(
                        force_bytes(user.pk)
                    ),
                    "token": account_activation_token.make_token(user),
                },
            )

            email = EmailMessage(
                mail_subject,
                message,
                to=[user.email],
            )

            email.send()

            messages.success(
                request,
                "Registration successful! Please check your email to activate your account."
            )

            return redirect("login")

    else:

        form = SignUpForm()

    return render(
        request,
        "accounts/signup.html",
        {
            "form": form,
        },
    )


def activate(request, uidb64, token):

    try:

        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = User.objects.get(pk=uid)

    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
    ):

        user = None

    if user is not None and account_activation_token.check_token(user, token):

        user.is_active = True
        user.save()

        messages.success(
            request,
            "Your account has been activated successfully. You can now log in."
        )

        return redirect("login")

    else:

        messages.error(
            request,
            "Activation link is invalid or has expired."
        )

        return redirect("signup")


def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():

            user = form.get_user()

            if not user.is_active:

                messages.error(
                    request,
                    "Please verify your email before logging in."
                )

                return redirect("login")

            login(request, user)

            messages.success(
                request,
                f"Welcome, {user.first_name or user.username}!"
            )

            return redirect("dashboard")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )


def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")