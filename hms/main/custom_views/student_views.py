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


def student_view_profile(request):
    if request.method == "GET":
        student = Student.objects.filter(client=request.user).first()
        return render(
            request,
            "student/profile.html",
            context={"student": student, "title": "view_profile"},
        )


def student_change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            client = request.user
            student = Student.objects.filter(client=client).first()
            current_password = form.cleaned_data.get("current_password")
            success = client.check_password(current_password)
            if success:
                new_password = form.cleaned_data.get("new_password")
                confirm_password = form.cleaned_data.get("confirm_password")
                if new_password == confirm_password:
                    client.set_password(new_password)
                    client.save()
                    student.client = client
                    student.save()
                    logout(request)
                    student = authenticate(
                        request, username=client.stakeholderID, password=new_password
                    )
                    login(request, student)
                    messages.success(request, f"password has been updated")
                    return redirect("/student/profile")
                else:
                    messages.error(
                        request, f"New password did not match confirm password"
                    )
                    return redirect("/student/change-password")
            else:
                messages.error(request, f"Current password entered is incorrect")
                return redirect("/student/change-password")

    else:
        form = ChangePasswordForm()
    return render(
        request,
        "student/change_password.html",
        context={"form": form, "title": "Password"},
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
        complaints = list(Complaint.objects.filter(student=student).all())
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

    pdf.drawString(350, 400, "Signature: ___________________")

    pdf.showPage()
    pdf.save()

    return response


def generate_student_passbook_pdf(request):

    student = Student.objects.filter(client=request.user).first()
    hall = student.hall

    student_passbook = StudentPassbook.objects.filter(student=student).first()
    payments = list(
        StudentPayment.objects.filter(student_passbook=student_passbook).all()
    )
    dues = list(Due.objects.filter(student_passbook=student_passbook).all())

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Student-Passbook.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    pdf.setFont("Helvetica", 12)

    y = 750
    pdf.drawString(200, y, "Dues")
    y = y - 30

    pdf.drawString(50, y, "Type")
    pdf.drawString(200, y, "Amount")
    pdf.drawString(350, y, "Time")

    y = y - 20
    for due in dues:
        pdf.drawString(50, y, "{}".format(due.type))
        pdf.drawString(200, y, "{}".format(due.demand))
        pdf.drawString(350, y, "{}".format(due.timestamp))
        y = y - 20

    y = y - 40
    pdf.drawString(200, y, "Payments")
    y = y - 30

    pdf.drawString(125, y, "Amount")
    pdf.drawString(275, y, "Time")

    y = y - 20
    for payment in payments:
        pdf.drawString(125, y, "{}".format(payment.fulfilled))
        pdf.drawString(275, y, "{}".format(payment.timestamp))
        y = y - 20

    pdf.drawString(350, 400, "Signature: ___________________")

    pdf.showPage()
    pdf.save()

    return response
