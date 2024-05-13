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


def Login(request):
    if request.method == "POST":

        # AuthenticationForm_can_also_be_used__

        stakeholderID = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=stakeholderID, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f" Welcome {stakeholderID}!")
            if request.user.role == "student":
                return redirect("/student/notice")
            elif request.user.role == "hall_manager":
                return redirect("/hall/landing")
            elif request.user.role == "mess_manager":
                return redirect("/mess/landing")
            elif request.user.role == "warden":
                return redirect("/warden/landing")
            elif request.user.role == "hmc_chairman":
                return redirect("/hmc/landing")
            else:
                redirect("/login")
        else:
            messages.info(request, "Either StakeholderID or Password is incorrect.")
    form = AuthenticationForm()
    return render(request, "auth/login.html", context={"form": form, "title": "log in"})


def Logout(request):
    logout(request)
    return redirect("/login")


def error_page(request):
    return render(request, "auth/error.html", {})


def entry(request):
    return redirect("/login")


def get_email(request):
    if request.method == "POST":
        form = SendMailForm(request.POST)
        if form.is_valid():
            stakeholderID = request.POST.get("stakeholderID")
            client = Client.objects.filter(stakeholderID=stakeholderID).first()
            if client is None:
                messages.error(request, "Account does not exist")
            else:
                email = client.email
                subject = "Change Account Password"
                message = f"Hi, click on this link to change your password http://127.0.0.1:8000/forgot-password/{stakeholderID}"
                email_from = "se.mhc.2024@gmail.com"
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list)
                messages.success(
                    request, f"Link to change password has been sent to {email}"
                )
                return redirect("/login")
    else:
        form = SendMailForm()
    return render(
        request,
        "auth/get_email.html",
        context={"form": form, "title": "email"},
    )


def forgot_password(request, stakeholderID):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            client = Client.objects.filter(stakeholderID=stakeholderID).first()
            new_password = form.cleaned_data.get("new_password")
            confirm_password = form.cleaned_data.get("confirm_password")
            if new_password == confirm_password:
                client.set_password(new_password)
                client.save()
                messages.success(
                    request, f"Your password has been updated {client.first_name}"
                )
                return redirect("/login")
            else:
                messages.error(request, f"New password did not match confirm password")
                return redirect(f"/forgot-password/{stakeholderID}")
    else:
        form = ForgotPasswordForm()
    return render(
        request,
        "auth/forgot_password.html",
        context={"form": form, "title": "Password"},
    )
