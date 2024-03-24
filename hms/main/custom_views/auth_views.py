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
            messages.success(request, f" welcome {stakeholderID} !!")
            if request.user.role == "student":
                return redirect("/student/notice")
            elif request.user.role == "hall_manager":
                return redirect("/hall/landing")
            elif request.user.role == "warden":
                return redirect("/warden/landing")
            else:
                redirect("/login")
        else:
            messages.info(request, f"account does not exist pls sign in")
    form = AuthenticationForm()
    return render(request, "auth/login.html", context={"form": form, "title": "log in"})


def Logout(request):
    logout(request)
    return redirect("login")


def error_page(request):
    return render(request, "auth/error.html", {})


def entry(request):
    return redirect("/login")
