from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test

from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from .forms import SignUpForm, ProfileForm
from .tokens import account_activation_token
from events.models import Participant


# ==========================================
# Signup
# ==========================================

def signup(request):

    if request.method == "POST":

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # User cannot login until email verification
            user.is_active = False
            user.save()

            # Create Participant Profile
            Participant.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}".strip() or user.username,
                email=user.email,
            )

            # Add to Participant Group
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


# ==========================================
# Account Activation
# ==========================================

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


# ==========================================
# Login
# ==========================================

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


# ==========================================
# Logout
# ==========================================

def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")

# ==========================================
# My Profile
# ==========================================

@login_required
def profile(request):

    participant = get_object_or_404(
        Participant,
        user=request.user,
    )

    context = {
        "participant": participant,
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )

@login_required
def edit_profile(request):

    participant = get_object_or_404(
        Participant,
        user=request.user,
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=participant,
        )

        if form.is_valid():

            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]
            request.user.email = form.cleaned_data["email"]

            request.user.save()

            participant = form.save(commit=False)

            participant.name = (
                f"{request.user.first_name} {request.user.last_name}".strip()
                or request.user.username
            )

            participant.email = request.user.email

            participant.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=participant,
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            },
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form,
        },
    )

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
# User List
# Admin + Organizer
# ==========================================

@login_required
@user_passes_test(is_admin_or_organizer)
def user_list(request):

    users = User.objects.all().order_by("username")

    return render(
        request,
        "accounts/user_list.html",
        {
            "users": users,
        },
    )


# ==========================================
# Change Role
# Admin Only
# ==========================================

@login_required
@user_passes_test(is_admin)
def change_role(request, user_id):

    user = get_object_or_404(
        User,
        pk=user_id,
    )

    # Superuser role cannot be changed
    if user.is_superuser:

        messages.error(
            request,
            "The Superuser role cannot be changed."
        )

        return redirect("user_list")

    if request.method == "POST":

        role = request.POST.get("role")

        # Remove existing groups
        user.groups.clear()

        # Add selected group
        group, created = Group.objects.get_or_create(
            name=role
        )

        user.groups.add(group)

        # Create or update Participant profile
        if role == "Participant":

            participant = Participant.objects.filter(
                email=user.email
            ).first()

            if participant:

                participant.user = user
                participant.name = (
                    f"{user.first_name} {user.last_name}".strip()
                    or user.username
                )
                participant.save()

            else:

                Participant.objects.create(
                    user=user,
                    name=(
                        f"{user.first_name} {user.last_name}".strip()
                        or user.username
                    ),
                    email=user.email,
                )

        messages.success(
            request,
            f"{user.username}'s role has been updated to {role}."
        )

        return redirect("user_list")

    groups = Group.objects.exclude(
        name="Admin"
    )

    return render(
        request,
        "accounts/change_role.html",
        {
            "selected_user": user,
            "groups": groups,
        },
    )
@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):

    user = get_object_or_404(
        User,
        pk=user_id,
    )

    # Prevent deleting yourself
    if user == request.user:

        messages.error(
            request,
            "You cannot delete your own account."
        )

        return redirect("user_list")

    # Prevent deleting superusers
    if user.is_superuser:

        messages.error(
            request,
            "Superuser accounts cannot be deleted."
        )

        return redirect("user_list")

    if request.method == "POST":

        username = user.username

        user.delete()

        messages.success(
            request,
            f"User '{username}' has been deleted successfully."
        )

        return redirect("user_list")

    return render(
        request,
        "accounts/delete_user.html",
        {
            "selected_user": user,
        },
    )