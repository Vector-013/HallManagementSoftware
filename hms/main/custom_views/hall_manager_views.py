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


def update_student_hall_dues():
    pass


# def update_student_profile(request, stakeholderID):
#     student = Student.objects.get(id=stakeholderID)

#     if request.method == "POST":
#         form = StudentRegistrationForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             return redirect("profile_success")  # Redirect to a success page
#     else:
#         form = StudentForm(instance=student)

#     return render(request, "edit_student_profile.html", {"form": form})


def allot_staff_duties():
    pass


def complaint_reports():
    pass


def create_atr(request):
    if request.method == "POST":
        form = ATRForm(request.POST)
        if form.is_valid():
            print(request.POST)
            complaint = form.cleaned_data.get("complaint")
            employee = form.cleaned_data.get("employee")
            report = form.cleaned_data.get("report")
            status = form.cleaned_data.get("status")
            atr = ATR(
                complaint=complaint, employee=employee, report=report, status=status
            )
            atr.save()
            messages.success(
                request,
                f"ATR created!",
            )
            return redirect("hall_view_complaints")
    else:
        form = ATRForm()
    return render(
        request,
        "hall_manager/create_atr.html",
        context={"form": form, "title": "register"},
    )


def hall_view_complaints(request):
    if request.method == "GET":
        hall_manager = HallManager.objects.filter(client=request.user)[0]
        complaints = Complaint.objects.filter(hall=hall_manager.hall)
        atrs = []
        for complaint in complaints:
            atr = ATR.objects.filter(complaint=complaint)[0]
            atrs.append(atr)
        print(complaints)
        data = zip(complaints, atrs)
        return render(
            request,
            "hall_manager/complaints.html",
            context={"data": data, "title": "GetComplaints"},
        )


def add_employee(request):
    if request.method == "POST":
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            hall_manager = HallManager.objects.filter(client=request.user)[0]
            stakeholderID = form.cleaned_data.get("stakeholderID")
            email = form.cleaned_data.get("email")
            address = form.cleaned_data.get("address")
            mobile = form.cleaned_data.get("mobile")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = "HallEmployee#123"
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
                "hall_employee",
            )
            salary = form.cleaned_data.get("salary")
            role = form.cleaned_data.get("role")
            client.is_active = True
            worker = HallEmployee(
                client=client, hall=hall_manager.hall, salary=salary, role=role
            )
            worker.save()
            messages.success(
                request,
                f"Employee {first_name} {last_name} Registered with ID {stakeholderID}",
            )
            return redirect("login")
    else:
        form = WorkerRegistrationForm()
    return render(
        request, "auth/register.html", context={"form": form, "title": "register"}
    )
