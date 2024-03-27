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
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def hall_manager(request):
    warden = Warden.objects.filter(client=request.user).first()
    hall = warden.hall
    hall_manager = HallManager.objects.filter(hall=hall).first()
    if hall_manager:
        return redirect("/hall/passbook")
    else:
        return redirect("/warden/register-hall-manager")

def delete_manager(request):
    warden = Warden.objects.filter(client=request.user).first()
    hall = warden.hall
    hall_manager = HallManager.objects.filter(hall=hall).first()
    mess_manager = MessManager.objects.filter(hall=hall).first()
    try:
        hall_manager_id = hall_manager.client.stakeholderID
    except:
        hall_manager_id = "Does not exist"
    try:
        mess_manager_id = mess_manager.client.stakeholderID
    except:
        mess_manager_id = "Does not exist"
    if request.method == "POST":
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            stakeholderID = form.cleaned_data.get("stakeholderID")
            password_to_confirm = form.cleaned_data.get("verify_password")
            client = Client.objects.filter(stakeholderID=stakeholderID).first()
            print(client.role)
            if client.role == "hall_manager":
                hall_manager = HallManager.objects.filter(client=client).first()
                hall_manager_id = "Does not exist"
                if (hall_manager and client.is_active):
                    success = request.user.check_password(password_to_confirm)
                    if success:
                        hall_manager.client.delete()
                        messages.success(request, f"Hall Manager with stakeholder ID {stakeholderID} has been deleted")
                    else:
                        messages.error(request, "Invalid password")
                else:
                    messages.error(request, "Nont enbfb")
            elif client.role == "mess_manager":
                mess_manager = MessManager.objects.filter(client=client).first()
                mess_manager_id = "Does not exist"
                if (mess_manager and client.is_active):
                    success = request.user.check_password(password_to_confirm)
                    if success:
                        mess_manager.client.delete()
                        messages.success(request, f"Mess Manager with stakeholder ID {stakeholderID} has been deleted")
                    else:
                        messages.error(request, "Invalid password")
            else:
                messages.error(request, f"No active mess manager found with stakeholder ID {stakeholderID}")
    else: 
        form = DeleteUserForm()
    return render(
        request,
        "warden/delete_manager.html",
        context={"form": form, "title": "verify", "hall_manager_id": hall_manager_id, "mess_manager_id": mess_manager_id},
    )

def mess_manager(request):
    warden = Warden.objects.filter(client=request.user).first()
    hall = warden.hall
    mess_manager = MessManager.objects.filter(hall=hall).first()
    if mess_manager:
        return redirect("/mess/passbook")
    else:
        return redirect("/warden/register-mess-manager")


def register_hall_manager(request):
    if request.method == "POST":
        form = ManagerRegistrationForm(request.POST)
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
            message = f"Hi, click on this link to verify your account http://127.0.0.1:8000/warden/verify-manager/{token}"
            email_from = "shreya.bose.in@gmail.com"
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request,
                f"Pls click on the link sent to {email} to complete registration",
            )
            return redirect("/warden/landing")
    else:
        form = ManagerRegistrationForm()
    return render(
        request,
        "warden/register_manager.html",
        context={"form": form, "title": "register"},
    )


def register_mess_manager(request):
    if request.method == "POST":
        form = ManagerRegistrationForm(request.POST)
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
                "mess_manager",
            )
            mess_manager = MessManager(client=client, hall=hall)
            mess_manager.save()
            subject = "Your account needs to be verified"
            message = f"Hi, click on this link to verify your account http://127.0.0.1:8000/warden/verify-manager/{token}"
            email_from = "shreya.bose.in@gmail.com"
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request,
                f"Pls click on the link sent to {email} to complete registration",
            )
            return redirect("/warden/landing")
    else:
        form = ManagerRegistrationForm()
    return render(
        request,
        "warden/register_manager.html",
        context={"form": form, "title": "register"},
    )


def verify_manager(request, token):
    client = Client.objects.filter(token=token).first()
    if client:
        client.is_active = True
        client.save()
        messages.info(request, "Your account has been verified")
        return redirect("/warden/landing")
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


def generate_salary(request):
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


def generate_mess_demand(request):
    if request.method == "POST":
        form = VerifyForm(request.POST)
        if form.is_valid():
            password_to_confirm = form.cleaned_data.get("verify_password")
            amount_per_student = form.cleaned_data.get("amount")
            client = request.user
            success = client.check_password(password_to_confirm)
            if success:
                # try:
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
                # except:
                messages.success(request, "Your password has been verified old codger")
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
    if request.method == "GET":
        warden = Warden.objects.filter(client=request.user).first()
        notices = Notice.objects.filter(hall=warden.hall)
        print(notices)
        return render(
            request,
            "warden/landing.html",
            context={"notices": notices, "title": "Notices"},
        )


def allot_budget(request):
    if request.method == "POST":
        form = AllotmentForm(request.POST)
        if form.is_valid():
            password_to_confirm = form.cleaned_data.get("verify_password")
            hall_allotment = form.cleaned_data.get("hall_allotment")
            mess_allotment = form.cleaned_data.get("mess_allotment")
            client = request.user
            success = client.check_password(password_to_confirm)
            if success:
                # try:
                warden = Warden.objects.filter(client=client).first()
                hall = warden.hall
                hall_passbook = HallPassbook.objects.filter(hall=hall).first()
                mess_passbook = MessPassbook.objects.filter(hall=hall).first()
                warden_passbook = WardenPassbook.objects.filter(hall=hall).first()
                hall_transaction = HallTransaction.objects.create(
                    type="allotment",
                    timestamp=datetime.now(),
                    amount=hall_allotment,
                    hall_passbook=hall_passbook,
                )
                mess_transaction = MessTransaction.objects.create(
                    type="allotment",
                    timestamp=datetime.now(),
                    amount=mess_allotment,
                    mess_passbook=mess_passbook,
                )
                warden_hall_transaction = WardenTransaction.objects.create(
                    type="hall_allotment",
                    timestamp=datetime.now(),
                    amount=hall_allotment,
                    warden_passbook=warden_passbook,
                )
                warden_mess_transaction = WardenTransaction.objects.create(
                    type="mess_allotment",
                    timestamp=datetime.now(),
                    amount=mess_allotment,
                    warden_passbook=warden_passbook,
                )
                # except:
                messages.success(request, "Your budgets have been alloted old codger")
                redirect("/warden/landing")

            # except:
            #     messages.error(request, "Connection issues")
            else:
                messages.error(request, "you are unreal")
                redirect("/login")
    else:
        form = AllotmentForm()

    return render(
        request,
        "warden/verify_password.html",
        context={"form": form, "title": "verify"},
    )


def generate_warden_passbook_pdf(request):

    print(request.user)
    warden = Warden.objects.filter(client=request.user).first()

    hall = hall_manager.hall
    warden_passbook = WardenPassbook.objects.filter(hall=hall).first()
    transactions_qset = WardenTransaction.objects.filter(
        warden_passbook=warden_passbook
    )
    transactions = list(transactions_qset.all())

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Hall-Passbook.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    pdf.setFont("Helvetica", 12)

    pdf.drawString(100, 750, "Type")
    pdf.drawString(300, 750, "Amount")
    pdf.drawString(500, 750, "Time")

    y = 730
    for transaction in transactions:
        pdf.drawString(100, y, "{}".format(transaction.type))
        pdf.drawString(300, y, "{}".format(transaction.amount))
        pdf.drawString(500, y, "{}".format(transaction.timestamp))
        y = y - 20

    pdf.line(50, 700, 550, 700)

    pdf.drawString(100, 400, "Signature: ___________________")

    pdf.showPage()
    pdf.save()

    return response
