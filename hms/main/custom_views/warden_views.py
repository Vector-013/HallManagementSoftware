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


def warden_hall_occupancy(request):
    if request.method == "GET":
        warden = Warden.objects.filter(client=request.user).first()
        hall = warden.hall
        rooms = list(Room.objects.filter(hall=hall))
        total_occupied = 0
        total_capacity = 0
        for room in rooms:
            total_capacity += room.sharing
            total_occupied += room.current_occupancy
        return render(
            request,
            "warden/hall_occupancy.html",
            context={
                "hall": hall,
                "rooms": rooms,
                "total_occupied": total_occupied,
                "total_capacity": total_capacity,
                "title": "view_hall",
            },
        )


def warden_view_students(request):
    if request.method == "GET":
        warden = Warden.objects.filter(client=request.user).first()
        hall = warden.hall
        students = list(Student.objects.filter(hall=hall))
        return render(
            request,
            "warden/view_students.html",
            context={"students": students, "title": "view_students"},
        )


def warden_view_employees(request):
    if request.method == "GET":
        warden = Warden.objects.filter(client=request.user).first()
        hall = warden.hall
        employees = list(HallEmployee.objects.filter(hall=hall))
        return render(
            request,
            "warden/view_employees.html",
            context={"employees": employees, "title": "view_employees"},
        )


def warden_view_profile(request):
    if request.method == "GET":
        warden = Warden.objects.filter(client=request.user).first()
        return render(
            request,
            "warden/profile.html",
            context={"warden": warden, "title": "view_profile"},
        )


def hall_manager(request):
    warden = Warden.objects.filter(client=request.user).first()
    hall = warden.hall
    hall_manager = HallManager.objects.filter(hall=hall).first()
    if hall_manager:
        return redirect("/hall/profile")
    else:
        messages.error(request, "No hall manager found.")
        return redirect("/warden/register-hall-manager")


def update_hall_manager_profile(request):
    warden = Warden.objects.filter(client=request.user).first()
    hall = warden.hall
    try:
        hall_manager = HallManager.objects.filter(hall=hall).first()
        client = hall_manager.client
        if request.method == "POST":
            form = UpdateHallManagerForm(request.POST, instance=hall_manager)
            if form.is_valid():
                client.stakeholderID = form.cleaned_data.get("stakeholderID")
                client.email = form.cleaned_data.get("email")
                client.address = form.cleaned_data.get("address")
                client.mobile = form.cleaned_data.get("mobile")
                client.first_name = form.cleaned_data.get("first_name")
                client.last_name = form.cleaned_data.get("last_name")
                hall_manager.hall = form.cleaned_data.get("hall")
                client.save()
                hall_manager.client = client
                hall_manager.save()
                messages.success(
                    request,
                    "Profile of Hall Manager Edited!",
                )
                return redirect("/hall/profile")  # Redirect to a success page
        else:
            form = UpdateHallManagerForm(
                initial={
                    "stakeholderID": client.stakeholderID,
                    "email": client.email,
                    "mobile": client.mobile,
                    "address": client.address,
                    "first_name": client.first_name,
                    "last_name": client.last_name,
                    "hall": hall_manager.hall,
                }
            )
            # print(form.instance)
            # form.instance = student

        return render(
            request, "warden/update_hall_manager_profile.html", {"form": form}
        )
    except:
        messages.error(request, "No hall manager found.")
        return redirect("/warden/register-hall-manager")


def mess_manager(request):
    warden = Warden.objects.filter(client=request.user).first()
    hall = warden.hall
    mess_manager = MessManager.objects.filter(hall=hall).first()
    if mess_manager:
        return redirect("/mess/profile")
    else:
        messages.error(request, "No mess manager found.")
        return redirect("/warden/register-mess-manager")


def update_mess_manager_profile(request):
    warden = Warden.objects.filter(client=request.user).first()
    hall = warden.hall
    try:
        mess_manager = MessManager.objects.filter(hall=hall).first()
        client = mess_manager.client
        if request.method == "POST":
            form = UpdateMessManagerForm(request.POST, instance=mess_manager)
            if form.is_valid():
                client.stakeholderID = form.cleaned_data.get("stakeholderID")
                client.email = form.cleaned_data.get("email")
                client.address = form.cleaned_data.get("address")
                client.mobile = form.cleaned_data.get("mobile")
                client.first_name = form.cleaned_data.get("first_name")
                client.last_name = form.cleaned_data.get("last_name")
                mess_manager.hall = form.cleaned_data.get("hall")
                client.save()
                mess_manager.client = client
                mess_manager.save()
                messages.success(request, "Profile of Mess Manager Edited!")
                return redirect("/mess/profile")  # Redirect to a success page
        else:

            form = UpdateMessManagerForm(
                initial={
                    "stakeholderID": client.stakeholderID,
                    "email": client.email,
                    "mobile": client.mobile,
                    "address": client.address,
                    "first_name": client.first_name,
                    "last_name": client.last_name,
                    "hall": mess_manager.hall,
                }
            )

        return render(
            request, "warden/update_mess_manager_profile.html", {"form": form}
        )
    except:
        messages.error(request, "No mess manager found.")
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
                            type="hostel",
                            timestamp=datetime.now(),
                            demand=amount_per_student,
                            student_passbook=student_passbook,
                        )
                        due.save()

                    messages.success(request, "Hall Fees have been generated")
                    redirect("/warden/landing")

                except:
                    messages.error(request, "Connection issues")
            else:
                messages.error(request, "Password Incorrect")
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

                transaction = HallTransaction(
                    type="salaries",
                    timestamp=datetime.now(),
                    amount=total,
                    hall_passbook=hall_passbook,
                )
                transaction.save()
                messages.success(request, "Hall salaries have been paid")
                redirect("/warden/landing")

            # except:
            #     messages.error(request, "Connection issues")
            else:
                messages.error(request, "Password Incorrect")
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
                messages.success(request, "Mess Fess have been generated")
                redirect("/warden/landing")

            # except:
            #     messages.error(request, "Connection issues")
            else:
                messages.error(request, "Password Incorrect")
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


def warden_change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            client = request.user
            warden = Warden.objects.filter(client=client).first()
            current_password = form.cleaned_data.get("current_password")
            success = client.check_password(current_password)
            if success:
                new_password = form.cleaned_data.get("new_password")
                confirm_password = form.cleaned_data.get("confirm_password")
                if new_password == confirm_password:
                    client.set_password(new_password)
                    client.save()
                    warden.client = client
                    warden.save()
                    logout(request)
                    warden = authenticate(
                        request, username=client.stakeholderID, password=new_password
                    )
                    login(request, warden)
                    messages.success(request, "Password has been updated")
                    return redirect("/warden/landing")
                else:
                    messages.error(
                        request, f"New password did not match confirm password"
                    )
                    return redirect("/warden/change-password")
            else:
                messages.error(request, f"Current password entered is incorrect")
                return redirect("/warden/change-password")

    else:
        form = ChangePasswordForm()
    return render(
        request,
        "warden/change_password.html",
        context={"form": form, "title": "Password"},
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
                messages.success(request, "Hall and Mess budgets have been alloted.")
                return redirect("/warden/passbook")

            # except:
            #     messages.error(request, "Connection issues")
            else:
                messages.error(request, "you are unreal")
                return redirect("/login")
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

    hall = warden.hall
    warden_passbook = WardenPassbook.objects.filter(hall=hall).first()
    transactions_qset = WardenTransaction.objects.filter(
        warden_passbook=warden_passbook
    )
    transactions = list(transactions_qset.all())

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Warden-Passbook.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 750, "Type")
    pdf.drawString(200, 750, "Amount")
    pdf.drawString(350, 750, "Time")

    y = 730
    for transaction in transactions:
        pdf.drawString(50, y, "{}".format(transaction.type))
        pdf.drawString(200, y, "{}".format(transaction.amount))
        pdf.drawString(350, y, "{}".format(transaction.timestamp))
        y = y - 20

    pdf.drawString(350, 400, "Signature: ___________________")

    pdf.showPage()
    pdf.save()

    return response


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
                if hall_manager and client.is_active:
                    success = request.user.check_password(password_to_confirm)
                    if success:
                        hall_manager.client.delete()
                        messages.success(
                            request,
                            f"Hall Manager with stakeholder ID {stakeholderID} has been deleted",
                        )
                    else:
                        messages.error(request, "Invalid password")
                else:
                    messages.error(request, "Nont enbfb")
            elif client.role == "mess_manager":
                mess_manager = MessManager.objects.filter(client=client).first()
                mess_manager_id = "Does not exist"
                if mess_manager and client.is_active:
                    success = request.user.check_password(password_to_confirm)
                    if success:
                        mess_manager.client.delete()
                        messages.success(
                            request,
                            f"Mess Manager with stakeholder ID {stakeholderID} has been deleted",
                        )
                    else:
                        messages.error(request, "Invalid password")
            else:
                messages.error(
                    request,
                    f"No active mess manager found with stakeholder ID {stakeholderID}",
                )
    else:
        form = DeleteUserForm()
    return render(
        request,
        "warden/delete_manager.html",
        context={
            "form": form,
            "title": "verify",
            "hall_manager_id": hall_manager_id,
            "mess_manager_id": mess_manager_id,
        },
    )
