from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from ..forms import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from ..models import *
import uuid


def hall_manager(request):
    warden = Warden.objects.filter(client=request.user).first()
    hall = warden.hall
    hall_manager = HallManager.objects.filter(hall=hall).first()
    if hall_manager:
        return render(request, "warden/hall_manager.html", context={"hall_manager": hall_manager})
    else:
        return redirect("/warden/register-hall-manager")

def register_hall_manager(request):
    if request.method == "POST":
        form = HallManagerRegistrationForm(request.POST)
        warden = Warden.objects.filter(client=request.user).first()
        if form.is_valid():
            print(request.POST)
            stakeholderID = form.cleaned_data.get("stakeholderID")
            email = form.cleaned_data.get("email")
            address = form.cleaned_data.get("address")
            mobile = form.cleaned_data.get("mobile")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            hall = warden.hall
            token = str(uuid.uuid4())
            client = Client.objects.create_user(
                stakeholderID,
                email,
                password,
                mobile,
                first_name,
                last_name,
                address,
                token,
                "hall_manager",
            )
            hall_manager = HallManager(client=client, hall=hall)
            hall_manager.save()
            subject = "Your account needs to be verified"
            message = f"Hi, click on this link to verify your account http://127.0.0.1:8000/warden/verify-hall-manager/{token}"
            email_from = "shreya.bose.in@gmail.com"
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request,
                f"Pls click on the link sent to {email} to complete registration",
            )
            return redirect("/warden/landing")
    else:
        form = HallManagerRegistrationForm()
    return render(
        request,
        "warden/register_hall_manager.html",
        context={"form": form, "title": "register"},
    )


def verify_hall_manager(request, token):
    client = Client.objects.filter(token=token).first()
    if client:
        client.is_active = True
        client.save()
        messages.info(request, "Your account has been verified")
        return redirect("/login")
    else:
        return redirect("/error")


def generate_hall_demand(request):
    if request.method == "POST":
        form = VerifyForm(request.POST)
        if form.is_valid():
            password_to_confirm = form.cleaned_data.get("verify_password")
            amount_per_student = form.cleaned_data.get("amount")
            client = request.user
            success = client.check_password(password_to_confirm)
            if success:
                try:
                    warden = Warden.objects.filter(client=client).first()
                    hall = warden.hall
                    students = list(hall.student_hall.all())

                    for student in students:
                        student_passbook = StudentPassbook.objects.filter(
                            student=student
                        ).first()
                        due = Due(
                            type="hall",
                            timestamp=datetime.now(),
                            demand=amount_per_student,
                            student_passbook=student_passbook,
                        )
                        due.save()

                    messages.success(
                        request, "Your password has been verified old codger"
                    )
                    redirect("/warden/landing")

                except:
                    messages.error(request, "Connection issues")
            else:
                messages.error(request, "you are unreal")
                redirect("/login")
    else:
        form = VerifyForm()

    return render(
        request,
        "warden/verify_password.html",
        context={"form": form, "title": "verify"},
    )


def generate_hall_salary(request):
    if request.method == "POST":
        form = ConfirmForm(request.POST)
        if form.is_valid():
            password_to_confirm = form.cleaned_data.get("verify_password")
            client = request.user
            success = client.check_password(password_to_confirm)
            if success:
                # try:
                warden = Warden.objects.filter(client=client).first()
                hall = warden.hall
                employees = list(hall.employee_hall.all())
                total = 0
                hall_passbook = HallPassbook.objects.filter(hall=hall).first()
                for employee in employees:
                    total = total + employee.salary

                expenditure = HallTransaction(
                    type="salaries",
                    timestamp=datetime.now(),
                    expenditure=total,
                    hall_passbook=hall_passbook,
                )
                expenditure.save()
                messages.success(request, "Hall employees have been paid old codger")
                redirect("/warden/landing")

            # except:
            #     messages.error(request, "Connection issues")
            else:
                messages.error(request, "you are unreal")
                redirect("/login")
    else:
        form = ConfirmForm()

    return render(
        request,
        "warden/verify_password.html",
        context={"form": form, "title": "verify"},
    )


def generate_mess_salary(request):
    if request.method == "POST":
        form = ConfirmForm(request.POST)
        if form.is_valid():
            password_to_confirm = form.cleaned_data.get("verify_password")
            client = request.user
            success = client.check_password(password_to_confirm)
            if success:
                # try:
                warden = Warden.objects.filter(client=client).first()
                hall = warden.hall
                employees = list(hall.mess_employee_hall.all())
                total = 0
                mess_passbook = MessPassbook.objects.filter(hall=hall).first()
                for employee in employees:
                    total = total + employee.salary

                expenditure = MessTransaction(
                    type="salaries",
                    timestamp=datetime.now(),
                    expenditure=total,
                    mess_passbook=mess_passbook,
                )
                expenditure.save()
                messages.success(request, "Mess employees have been paid old codger")
                redirect("/warden/landing")

            # except:
            #     messages.error(request, "Connection issues")
            else:
                messages.error(request, "you are unreal")
                redirect("/login")
    else:
        form = ConfirmForm()

    return render(
        request,
        "warden/verify_password.html",
        context={"form": form, "title": "verify"},
    )


def generate_mess_demand(request):
    if request.method == "POST":
        form = VerifyForm(request.POST)
        if form.is_valid():
            password_to_confirm = form.cleaned_data.get("verify_password")
            amount_per_student = form.cleaned_data.get("amount")
            client = request.user
            success = client.check_password(password_to_confirm)
            if success:
                try:
                    warden = Warden.objects.filter(client=client).first()
                    hall = warden.hall
                    students = list(hall.student_hall.all())

                    for student in students:
                        student_passbook = StudentPassbook.objects.filter(
                            student=student
                        ).first()
                        due = Due(
                            type="mess",
                            timestamp=datetime.now(),
                            demand=amount_per_student,
                            student_passbook=student_passbook,
                        )
                        due.save()
                except:
                    messages.success(
                        request, "Your password has been verified old codger"
                    )
                    redirect("/warden/landing")

            # except:
            #     messages.error(request, "Connection issues")
            else:
                messages.error(request, "you are unreal")
                redirect("/login")
    else:
        form = VerifyForm()

    return render(
        request,
        "warden/verify_password.html",
        context={"form": form, "title": "verify"},
    )


def warden_landing(request):
    return render(request, "warden/landing.html")
