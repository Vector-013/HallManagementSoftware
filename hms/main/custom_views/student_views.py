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


def view_profile(request):
    if request.method == "GET":
        student = Student.objects.filter(client=request.user)[0]
        return render(
            request,
            "student/student_profile.html",
            context={"student": student, "title": "view_profile"},
        )


def make_complaints(request):
    if request.method == "POST":
        form = ComplaintRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = Student.objects.filter(client=request.user).first()
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            category = form.cleaned_data.get("category")
            image = request.FILES["image"]
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
            return redirect("/student/view-complaints")
    else:
        form = ComplaintRegistrationForm()

    print(request)
    return render(
        request,
        "student/make_complaints.html",
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
        student = Student.objects.filter(client=request.user).first()
        notices = Notice.objects.filter(hall=student.hall)
        print(notices)
        return render(
            request,
            "student/view_notice.html",
            context={"notices": notices, "title": "Notices"},
        )


def generate_atr_pdf(request, pk):

    complaint = Complaint.objects.get(pk=pk)
    atr = ATR.objects.filter(complaint=complaint).first()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="ATR Report.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    pdf.setFont("Helvetica", 12)

    pdf.drawString(100, 750, "Complaint: {}".format(complaint.title))
    pdf.drawString(100, 730, "{}".format(atr.report))

    pdf.line(50, 630, 550, 630)

    pdf.showPage()
    pdf.save()

    return response
