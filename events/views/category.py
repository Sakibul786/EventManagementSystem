from django.shortcuts import render, redirect, get_object_or_404
from events.models import Category
from events.forms import CategoryForm
from django.contrib import messages


def category_list(request):
    categories = Category.objects.all()
    return render(
        request,
        "events/category/category_list.html",
        {"categories": categories},
    )


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect("category_list")
    else:
        form = CategoryForm()

    return render(
        request,
        "events/category/category_form.html",
        {"form": form},
    )


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "events/category/category_form.html",
        {"form": form},
    )


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("category_list")

    return render(
        request,
        "events/category/category_confirm_delete.html",
        {"category": category},
    )