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
from django.contrib.auth.decorators import permission_required


@permission_required("main.is_warden", "/login")
@permission_required("main.is_mess_manager", "/login")
def mess_view_profile(request):
    if request.method == "GET":
        try:
            mess_manager = MessManager.objects.filter(client=request.user).first()
            hall = mess_manager.hall
            template = "mess_manager/base.html"
        except:
            warden = Warden.objects.filter(client=request.user).first()
            hall = warden.hall
            mess_manager = MessManager.objects.filter(hall=hall).first()
            template = "warden/base.html"
        return render(
            request,
            "mess_manager/profile.html",
            context={
                "template": template,
                "mess_manager": mess_manager,
                "title": "view_profile",
            },
        )


@permission_required("main.is_mess_manager", "/login")
def mess_landing(request):
    if request.method == "GET":
        mess_manager = MessManager.objects.filter(client=request.user).first()
        notices = Notice.objects.filter(hall=mess_manager.hall)
        print(notices)
        return render(
            request,
            "mess_manager/landing.html",
            context={"notices": notices, "title": "Notices"},
        )


@permission_required("main.is_mess_manager", "/login")
def mess_change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            client = request.user
            mess_manager = MessManager.objects.filter(client=client).first()
            current_password = form.cleaned_data.get("current_password")
            success = client.check_password(current_password)
            if success:
                new_password = form.cleaned_data.get("new_password")
                confirm_password = form.cleaned_data.get("confirm_password")
                if new_password == confirm_password:
                    client.set_password(new_password)
                    client.save()
                    mess_manager.client = client
                    mess_manager.save()
                    logout(request)
                    mess_manager = authenticate(
                        request, username=client.stakeholderID, password=new_password
                    )
                    login(request, mess_manager)
                    messages.success(request, f"password has been updated")
                    return redirect("/mess/profile")
                else:
                    messages.error(
                        request, f"New password did not match confirm password"
                    )
                    return redirect("/mess/change-password")
            else:
                messages.error(request, f"Current password entered is incorrect")
                return redirect("/mess/change-password")

    else:
        form = ChangePasswordForm()
    return render(
        request,
        "mess_manager/change_password.html",
        context={"form": form, "title": "Password"},
    )


@permission_required("main.is_mess_manager", "/login")
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


@permission_required("main.is_student", "/login")
@permission_required("main.is_mess_manager", "/login")
def view_menu(request):
    if request.method == "GET":
        try:
            mess_manager = MessManager.objects.filter(client=request.user).first()
            hall = mess_manager.hall
            template = "mess_manager/base.html"
        except:
            student = Student.objects.filter(client=request.user).first()
            hall = student.hall
            mess_manager = MessManager.objects.filter(hall=hall).first()
            template = "student/base.html"
        menu = Menu.objects.filter(hall=hall).first()
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
            context={
                "items": items,
                "month": month,
                "template": template,
                "title": "Menu",
            },
        )


@permission_required("main.is_mess_manager", "/login")
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
                amount=total,
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


@permission_required("main.is_warden", "/login")
@permission_required("main.is_mess_manager", "/login")
def generate_mess_passbook_pdf(request):

    try:
        mess_manager = MessManager.objects.filter(client=request.user).first()
        hall = mess_manager.hall
    except:
        warden = Warden.objects.filter(client=request.user).first()
        hall = warden.hall

    mess_passbook = MessPassbook.objects.filter(hall=hall).first()
    transactions_qset = MessTransaction.objects.filter(mess_passbook=mess_passbook)
    transactions = list(transactions_qset.all())

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Mess-Passbook.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 750, "Type")
    pdf.drawString(200, 750, "Amount")
    pdf.drawString(350, 750, "Time")

    y = 730
    for transaction in transactions:
        pdf.drawString(50, y, "{}".format(transaction.type))
        pdf.drawString(200, y, "{}".format(transaction.amount))
        pdf.drawString(350, y, "{}".format(transaction.timestamp))
        y = y - 20

    pdf.drawString(300, 400, "Signature: ___________________")

    pdf.showPage()
    pdf.save()

    return response
