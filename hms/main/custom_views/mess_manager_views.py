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
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def mess_landing(request):
    return render(request, "mess_manager/landing.html")


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


def view_menu(request):
    if request.method == "GET":
        mess_manager = MessManager.objects.filter(client=request.user).first()
        menu = Menu.objects.filter(hall=mess_manager.hall)[0]
        month = menu.month
        items = [
            [
                "Monday",
                menu.monday_breakfast,
                menu.monday_lunch,
                menu.monday_snacks,
                menu.monday_dinner,
            ],
            [
                "Tuesday",
                menu.tuesday_breakfast,
                menu.tuesday_lunch,
                menu.tuesday_snacks,
                menu.tuesday_dinner,
            ],
            [
                "Wednesday",
                menu.wednesday_breakfast,
                menu.wednesday_lunch,
                menu.wednesday_snacks,
                menu.wednesday_dinner,
            ],
            [
                "Thursday",
                menu.thursday_breakfast,
                menu.thursday_lunch,
                menu.thursday_snacks,
                menu.thursday_dinner,
            ],
            [
                "Friday",
                menu.friday_breakfast,
                menu.friday_lunch,
                menu.friday_snacks,
                menu.friday_dinner,
            ],
            [
                "Saturday",
                menu.saturday_breakfast,
                menu.saturday_lunch,
                menu.saturday_snacks,
                menu.saturday_dinner,
            ],
            [
                "Sunday",
                menu.sunday_breakfast,
                menu.sunday_lunch,
                menu.sunday_snacks,
                menu.sunday_dinner,
            ],
        ]
        return render(
            request,
            "mess_manager/menu.html",
            context={"items": items, "month": month, "title": "Menu"},
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
            mess_passbook = hall.mess_passbook

            MessTransaction.objects.create(
                type="rations",
                timestamp=datetime.now(),
                expenditure=total,
                mess_passbook=mess_passbook,
            )
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


def generate_mess_passbook_pdf(request):

    mess_manager = MessManager.objects.filter(client=request.user).first()

    hall = mess_manager.hall
    mess_passbook = MessPassbook.objects.filter(hall=hall).first()
    expenditures_qset = MessTransaction.objects.filter(mess_passbook=mess_passbook)
    expenditures = list(expenditures_qset.all())

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Hall-Passbook.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    pdf.setFont("Helvetica", 12)

    pdf.drawString(100, 750, "Title: {}".format("Type"))
    y = 730
    for expenditure in expenditures:
        pdf.drawString(100, y, "Details: {}".format(expenditure.type))
        y = y - 20

    pdf.drawString(300, 750, "Title: {}".format("Expenditure"))
    y = 730
    for expenditure in expenditures:
        pdf.drawString(300, y, "Details: {}".format(expenditure.amount))
        y = y - 20

    pdf.drawString(500, 750, "Title: {}".format("Time"))
    y = 730
    for expenditure in expenditures:
        pdf.drawString(500, y, "Details: {}".format(expenditure.timestamp))
        y = y - 20

    pdf.line(50, 700, 550, 700)

    pdf.drawString(100, 400, "Signature: ___________________")

    pdf.showPage()
    pdf.save()

    return response
