from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import uuid
from ..models import *
from ..forms import *


def make_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            mess_manager = MessManager.objects.filter(client=request.user).first()
            hall = mess_manager.hall
            menu = form.save(commit=False)
            menu.hall = hall
            menu.save()
            messages.success(
                request,
                f"Menu made!",
            )
            return redirect("/mess/menu")
    else:
        form = MenuForm()
    return render(
        request,
        "mess_manager/make_menu.html",
        context={"form": form, "title": "register"},
    )


def mess_menu(request):
    if request.method == "GET":
        mess_manager = MessManager.objects.filter(client=request.user).first()
        menu = Menu.objects.filter(hall=mess_manager.hall)[0]
        items = {
            "Month": menu.month,
            "Monday": [
                menu.monday_breakfast,
                menu.monday_lunch,
                menu.monday_snacks,
                menu.monday_dinner,
            ],
            "Tuesday": [
                menu.tuesday_breakfast,
                menu.tuesday_lunch,
                menu.tuesday_snacks,
                menu.tuesday_dinner,
            ],
            "Wednesday": [
                menu.wednesday_breakfast,
                menu.wednesday_lunch,
                menu.wednesday_snacks,
                menu.wednesday_dinner,
            ],
            "Thursday": [
                menu.thursday_breakfast,
                menu.thursday_lunch,
                menu.thursday_snacks,
                menu.thursday_dinner,
            ],
            "Friday": [
                menu.friday_breakfast,
                menu.friday_lunch,
                menu.friday_snacks,
                menu.friday_dinner,
            ],
            "Saturday": [
                menu.saturday_breakfast,
                menu.saturday_lunch,
                menu.saturday_snacks,
                menu.saturday_dinner,
            ],
            "Sunday": [
                menu.sunday_breakfast,
                menu.sunday_lunch,
                menu.sunday_snacks,
                menu.sunday_dinner,
            ],
        }
        return render(
            request,
            "mess_manager/menu.html",
            context={"items": items, "title": "Menu"},
        )


def add_ration(request):
    if request.method == "POST":
        form = RationForm(request.POST)
        if form.is_valid():
            mess_manager = MessManager.objects.filter(client=request.user).first()
            hall = mess_manager.hall
            ration = form.save(commit=False)
            ration.hall = hall
            total = (
                ration.qt1 * ration.rate1
                + ration.qt2 * ration.rate2
                + ration.qt3 * ration.rate3
                + ration.qt4 * ration.rate4
                + ration.qt5 * ration.rate5
            )
            ration.total = total
            ration.save()
            messages.success(
                request,
                f"Ration added!",
            )
            return redirect("/mess/passbook")
    else:
        form = RationForm()
    return render(
        request,
        "mess_manager/add_ration.html",
        context={"form": form, "title": "Add Ration"},
    )
