from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from events.models import Category
from events.forms import CategoryForm


# -----------------------------
# Role Checking Function
# -----------------------------

def is_admin(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Admin").exists()
    )


# -----------------------------
# Category List
# -----------------------------

@login_required
@user_passes_test(is_admin)
def category_list(request):

    categories = Category.objects.all()

    return render(
        request,
        "events/category/category_list.html",
        {
            "categories": categories,
        },
    )


# -----------------------------
# Create Category
# -----------------------------

@login_required
@user_passes_test(is_admin)
def category_create(request):

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Category created successfully."
            )

            return redirect("category_list")

    else:

        form = CategoryForm()

    return render(
        request,
        "events/category/category_form.html",
        {
            "form": form,
        },
    )


# -----------------------------
# Update Category
# -----------------------------

@login_required
@user_passes_test(is_admin)
def category_update(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk,
    )

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            instance=category,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Category updated successfully."
            )

            return redirect("category_list")

    else:

        form = CategoryForm(
            instance=category,
        )

    return render(
        request,
        "events/category/category_form.html",
        {
            "form": form,
        },
    )


# -----------------------------
# Delete Category
# -----------------------------

@login_required
@user_passes_test(is_admin)
def category_delete(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk,
    )

    if request.method == "POST":

        category.delete()

        messages.success(
            request,
            "Category deleted successfully."
        )

        return redirect("category_list")

    return render(
        request,
        "events/category/category_confirm_delete.html",
        {
            "category": category,
        },
    )