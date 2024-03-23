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


def index(request):
    return render(request, "index.html", {"title": "index"})


def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
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
            client = Client.objects.create_user(
                stakeholderID,
                email,
                password,
                mobile,
                first_name,
                last_name,
                address,
                token,
                "student",
            )
            student = Student(client=client, hall=hall)
            student.save()
            subject = "Your account needs to be verified"
            message = f"Hi, click on this link to verify your account http://127.0.0.1:8000/verify/{token}"
            email_from = "shreya.bose.in@gmail.com"
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request,
                f"Pls click on the link sent to {email} to complete registration",
            )
            return redirect("login")
    else:
        form = StudentRegistrationForm()
    return render(request, "register.html", context={"form": form, "title": "register"})


def Login(request):
    if request.method == "POST":

        # AuthenticationForm_can_also_be_used__

        stakeholderID = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=stakeholderID, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f" welcome {stakeholderID} !!")
            return redirect("/")
        else:
            messages.info(request, f"account does not exist pls sign in")
    form = AuthenticationForm()
    return render(request, "login.html", context={"form": form, "title": "log in"})


def Logout(request):
    logout(request)
    return redirect("login")


def verify(request, token):
    client = Client.objects.filter(token=token).first()
    student = Student.objects.filter(client=client)[0]
    if client:
        client.is_active = True
        client.save()
        passbook = StudentPassbook(student=student)
        passbook.save()
        messages.info(request, "Your account has been verified")
        return redirect("/login")
    else:
        return redirect("/error")


def error_page(request):
    return render(request, "error.html", {})
