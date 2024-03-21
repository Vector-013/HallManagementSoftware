from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .models import *
import uuid


def index(request):
    return render(request, "index.html", {"title": "index"})


def register(request):
    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            address = form.cleaned_data.get("address")
            role = form.cleaned_data.get("role")
            mobile = form.cleaned_data.get("mobile")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            token = str(uuid.uuid4())
            form.Meta.model.objects.create_user(
                username,
                email,
                password,
                mobile,
                first_name,
                last_name,
                address,
                token,
                role,
            )
            subject = "Your account needs to be verified"
            message = f"Hi, click on this link to verify your account http://127.0.0.1:8000/verify/{token}"
            email_from = "shreya.bose.in@gmail.com"
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request, f"Your account has been created ! You are now able to log in"
            )
            return redirect("login")
    else:
        form = ClientRegistrationForm()
    return render(request, "register.html", context={"form": form, "title": "register"})


def Login(request):
    if request.method == "POST":

        # AuthenticationForm_can_also_be_used__

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f" welcome {username} !!")
            return redirect("/")
        else:
            messages.info(request, f"account done not exit plz sign in")
    form = AuthenticationForm()
    return render(request, "login.html", context={"form": form, "title": "log in"})


def Logout(request):
    logout(request)
    return redirect("login")


def verify(request, token):
    client = Client.objects.filter(token=token).first()
    if client:
        client.is_active = True
        client.save()
        messages.info(request, "Your account has been verified")
        return redirect("/login")
    else:
        return redirect("/error")


def error_page(request):
    return render(request, "error.html", {})


def make_complaints(request):
    if request.method == "POST":
        form = ComplaintRegistrationForm(request.POST)
        if form.is_valid():
            student = Student.objects.filter(client=request.user)[0]
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            role = form.cleaned_data.get("role")
            obj = Complaint(
                title=title,
                content=content,
                hall=student.hall,
                student=student,
                role=role,
            )
            print(obj)
            obj.save()
            messages.success(request, f"Your complaint has been registered.")
            return redirect("/view-complaints")
    else:
        form = ComplaintRegistrationForm()

    print(request)
    return render(
        request,
        "student/make-complaints.html",
        context={"form": form, "title": "Complaint"},
    )


def view_complaints(request):
    if request.method == "GET":
        student = Student.objects.filter(client=request.user)[0]
        complaints = Complaint.objects.filter(student=student)
        print(complaints)
        return render(
            request,
            "student/view_complaints.html",
            context={"complaints": complaints, "title": "GetComplaints"},
        )


def notice_student(request):
    if request.method == "GET":
        student = Student.objects.filter(client=request.user)[0]
        notices = Notice.objects.filter(hall=student.hall)
        print(notices)
        return render(
            request,
            "student/notice.html",
            context={"notices": notices, "title": "GetComplaints"},
        )
