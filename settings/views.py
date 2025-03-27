from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PointSetting, BusinessHours, Category
from .forms import PointSettingForm, BusinessHoursForm, CategoryForm

def settings_view(request):
    points, _ = PointSetting.objects.get_or_create()
    hours, _ = BusinessHours.objects.get_or_create()
    categories = Category.objects.all()

    if request.method == "POST":
        points_form = PointSettingForm(request.POST, instance=points)
        hours_form = BusinessHoursForm(request.POST, instance=hours)
        category_form = CategoryForm(request.POST, request.FILES)

        if points_form.is_valid() and hours_form.is_valid():
            points_form.save()
            hours_form.save()
            messages.success(request, "Configurações salvas com sucesso!")
            return redirect("settings")

        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Categoria adicionada com sucesso!")
            return redirect("settings")

    else:
        points_form = PointSettingForm(instance=points)
        hours_form = BusinessHoursForm(instance=hours)
        category_form = CategoryForm()

    return render(request, "settings/settings_form.html", {
        "points_form": points_form,
        "hours_form": hours_form,
        "category_form": category_form,
        "categories": categories,
    })


def delete_category(request, pk):
    if request.method == "POST":
        category = Category.objects.filter(pk=pk).first()
        
        if category:
            category.delete()
            messages.success(request, "Categoria excluida com sucesso!")
        else:
            messages.error(request, "Categoria nao encontrada!")
            
    return redirect("settings")