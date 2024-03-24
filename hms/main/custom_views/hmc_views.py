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


def register_warden(request):
    if request.method == "POST":
        form = WardenRegistrationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            stakeholderID = form.cleaned_data.get("stakeholderID")
            email = form.cleaned_data.get("email")
            address = form.cleaned_data.get("address")
            mobile = form.cleaned_data.get("mobile")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            hall = form.cleaned_data.get("hall")
            token = str(uuid.uuid4())
            department = form.cleaned_data.get("department")
            designation = form.cleaned_data.get("designation")
            posts_held = form.cleaned_data.get("posts_held")
            client = Client.objects.create_user(
                stakeholderID,
                email,
                password,
                mobile,
                first_name,
                last_name,
                address,
                token,
                "warden",
            )
            warden = Warden(
                client=client,
                hall=hall,
                department=department,
                designation=designation,
                posts_held=posts_held,
            )
            warden.save()
            subject = "Your account needs to be verified"
            message = f"Hi, click on this link to verify your account http://127.0.0.1:8000/verify-hall-manager/{token}"
            email_from = "shreya.bose.in@gmail.com"
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request,
                f"Pls click on the link sent to {email} to complete registration",
            )
            return redirect("warden/landing")
    else:
        form = WardenRegistrationForm()
    return render(
        request,
        "hmc/register_warden.html",
        context={"form": form, "title": "register"},
    )


def verify_warden(request, token):
    client = Client.objects.filter(token=token).first()
    if client:
        client.is_active = True
        client.save()
        messages.info(request, "Your account has been verified")
        return redirect("/login")
    else:
        return redirect("/error")


def hmc_landing(request):
    return render(request, "hmc/landing.html")
