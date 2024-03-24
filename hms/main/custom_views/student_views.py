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

@login_required
def make_complaints(request):
    if request.method == "POST":
        form = ComplaintRegistrationForm(request.POST)
        if form.is_valid():
            student = Student.objects.filter(client=request.user)[0]
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            category = form.cleaned_data.get("category")
            image = form.cleaned_data.get("image")
            obj = Complaint(
                title=title,
                content=content,
                hall=student.hall,
                student=student,
                category=category,
                image=image,
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

@login_required
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

@login_required
def notice_student(request):
    return render(
        request,
        "student/notice.html",
    )
    
