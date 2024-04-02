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
from django.http import FileResponse
from reportlab.pdfgen import canvas
from ..models import *
from ..forms import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from datetime import date
from django.contrib.auth.decorators import permission_required


@permission_required("main.is_hall", "/login")
def manager_hall_occupancy(request):
    if request.method == "GET":
        try:
            hall_manager = HallManager.objects.filter(client=request.user).first()
            hall = hall_manager.hall
            template = "hall_manager/base.html"
        except:
            warden = Warden.objects.filter(client=request.user).first()
            hall = warden.hall
            template = "warden/base.html"
        rooms = list(Room.objects.filter(hall=hall))
        total_occupied = 0
        total_capacity = 0
        for room in rooms:
            total_capacity += room.sharing
            total_occupied += room.current_occupancy
        return render(
            request,
            "hall_manager/hall_occupancy.html",
            context={
                "hall": hall,
                "rooms": rooms,
                "template": template,
                "total_occupied": total_occupied,
                "total_capacity": total_capacity,
                "title": "view_hall",
            },
        )


@permission_required("main.is_hall", "/login")
def manager_view_students(request):
    if request.method == "GET":
        try:
            hall_manager = HallManager.objects.filter(client=request.user).first()
            hall = hall_manager.hall
            template = "hall_manager/base.html"
        except:
            warden = Warden.objects.filter(client=request.user).first()
            hall = warden.hall
            template = "warden/base.html"
        students = list(Student.objects.filter(hall=hall))
        return render(
            request,
            "hall_manager/view_students.html",
            context={
                "template": template,
                "students": students,
                "title": "view_students",
            },
        )


@permission_required("main.is_hall", "/login")
def manager_view_employees(request):
    if request.method == "GET":
        try:
            hall_manager = HallManager.objects.filter(client=request.user).first()
            hall = hall_manager.hall
            template = "hall_manager/base.html"
        except:
            warden = Warden.objects.filter(client=request.user).first()
            hall = warden.hall
            template = "warden/base.html"
        employees = list(HallEmployee.objects.filter(hall=hall))
        return render(
            request,
            "hall_manager/view_employees.html",
            context={
                "template": template,
                "employees": employees,
                "title": "view_employees",
            },
        )


@permission_required("main.is_hall", "/login")
def hall_view_profile(request):
    if request.method == "GET":
        try:
            hall_manager = HallManager.objects.filter(client=request.user).first()
            hall = hall_manager.hall
            template = "hall_manager/base.html"
        except:
            warden = Warden.objects.filter(client=request.user).first()
            hall = warden.hall
            hall_manager = HallManager.objects.filter(hall=hall).first()
            template = "warden/base.html"
        return render(
            request,
            "hall_manager/profile.html",
            context={
                "hall_manager": hall_manager,
                "template": template,
                "title": "view_profile",
            },
        )


@permission_required("main.is_hall_manager", "/login")
def update_student_profile(request, stakeholderID):
    client = Client.objects.filter(stakeholderID=stakeholderID).first()
    student = Student.objects.filter(client=client).first()
    if request.method == "POST":
        form = UpdateStudentForm(request.POST, instance=student)
        if form.is_valid():
            client.stakeholderID = form.cleaned_data.get("stakeholderID")
            client.email = form.cleaned_data.get("email")
            client.address = form.cleaned_data.get("address")
            client.mobile = form.cleaned_data.get("mobile")
            client.first_name = form.cleaned_data.get("first_name")
            client.last_name = form.cleaned_data.get("last_name")
            student.hall = form.cleaned_data.get("hall")
            client.save()
            student.client = client
            student.save()
            messages.success(
                request,
                f"Student Profile Edited!",
            )
            return redirect("/hall/search-student")  # Redirect to a success page
    else:
        form = UpdateStudentForm(
            initial={
                "stakeholderID": stakeholderID,
                "email": client.email,
                "mobile": client.mobile,
                "address": client.address,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "hall": student.hall,
            }
        )
        # print(form.instance)
        # form.instance = student

    return render(request, "hall_manager/update_student_profile.html", {"form": form})


@permission_required("main.is_hall_manager", "/login")
def update_employee_profile(request, stakeholderID):
    client = Client.objects.filter(stakeholderID=stakeholderID).first()
    employee = HallEmployee.objects.filter(client=client).first()
    if request.method == "POST":
        form = UpdateEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            client.stakeholderID = form.cleaned_data.get("stakeholderID")
            client.email = form.cleaned_data.get("email")
            client.address = form.cleaned_data.get("address")
            client.mobile = form.cleaned_data.get("mobile")
            client.first_name = form.cleaned_data.get("first_name")
            client.last_name = form.cleaned_data.get("last_name")
            employee.hall = form.cleaned_data.get("hall")
            employee.role = form.cleaned_data.get("role")
            employee.salary = form.cleaned_data.get("salary")
            employee.unpaid_monthly_leaves = form.cleaned_data.get(
                "unpaid_monthly_leaves"
            )
            employee.paid_monthly_leaves = form.cleaned_data.get("paid_monthly_leaves")
            client.save()
            employee.client = client
            employee.save()
            messages.success(
                request,
                f"Employee Profile Edited!",
            )
            return redirect("/hall/search-employee")
    else:
        form = UpdateEmployeeForm(
            initial={
                "stakeholderID": stakeholderID,
                "email": client.email,
                "mobile": client.mobile,
                "address": client.address,
                "first_name": client.first_name,
                "last_name": client.last_name,
                "hall": employee.hall,
                "role": employee.role,
                "salary": employee.salary,
                "unpaid_monthly_leaves": employee.unpaid_monthly_leaves,
                "paid_monthly_leaves": employee.paid_monthly_leaves,
            }
        )
        # print(form.instance)
        # form.instance = student

    return render(request, "hall_manager/update_student_profile.html", {"form": form})


@permission_required("main.is_hall_manager", "/login")
def search_user(request):
    if request.method == "POST":
        form = UserSearchForm(request.POST)
        if form.is_valid():
            stakeholderID = form.cleaned_data.get("stakeholderID")
            try:
                client = Client.objects.filter(stakeholderID=stakeholderID).first()
                print(client.role)
                if client.role == "student":
                    return redirect(f"/hall/update-student-profile/{stakeholderID}")
                elif client.role == "hall_employee":
                    return redirect(f"/hall/update-employee-profile/{stakeholderID}")
                else:
                    print("popo")
                    messages.MessageFailure(
                        request,
                        f"User not found",
                    )
                    return redirect("/hall/search-user")

            except:
                messages.MessageFailure(
                    request,
                    f"User not found",
                )
                return redirect("/hall/search-user")
    else:
        form = UserSearchForm()
    return render(
        request,
        "hall_manager/search_student.html",
        context={"form": form, "title": "register"},
    )


@permission_required("main.is_hall_manager", "/login")
def create_atr(request):
    if request.method == "POST":
        form = ATRForm(request.POST)
        if form.is_valid():
            print(request.POST)
            complaint = form.cleaned_data.get("complaint")
            complaint.status = True
            complaint.save()
            employee = form.cleaned_data.get("employee")
            report = form.cleaned_data.get("report")
            atr = ATR(complaint=complaint, employee=employee, report=report)
            atr.save()
            messages.success(
                request,
                f"ATR created!",
            )
            return redirect("/hall/complaints")
    else:
        form = ATRForm()
    return render(
        request,
        "hall_manager/create_atr.html",
        context={"form": form, "title": "register"},
    )


@permission_required("main.is_hall", "/login")
def hall_complaints(request):
    if request.method == "GET":
        try:
            hall_manager = HallManager.objects.filter(client=request.user).first()
            hall = hall_manager.hall
            template = "hall_manager/base.html"
        except:
            warden = Warden.objects.filter(client=request.user).first()
            hall = warden.hall
            template = "warden/base.html"

        complaints = list(Complaint.objects.filter(hall=hall).all())
        return render(
            request,
            "hall_manager/complaints.html",
            context={
                "complaints": complaints,
                "template": template,
                "title": "Complaints",
            },
        )


@permission_required("main.is_hall_manager", "/login")
def add_employee(request):
    if request.method == "POST":
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            hall_manager = HallManager.objects.filter(client=request.user).first()
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
            return redirect("/hall/landing")
    else:
        form = WorkerRegistrationForm()
    return render(
        request,
        "hall_manager/add_employee.html",
        context={"form": form, "title": "register"},
    )


@permission_required("main.is_hall_manager", "/login")
def approve_leaves(request):
    if request.method == "POST":
        form = LeaveForm(request.POST, request.FILES)
        if form.is_valid():
            stakeholderID = form.cleaned_data.get("stakeholderID")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            employee_client = Client.objects.filter(stakeholderID=stakeholderID).first()
            employee = HallEmployee.objects.filter(client=employee_client).first()
            monthly_leaves = abs((end_date - start_date).days)
            try:
                uploads = request.FILES["uploads"]
                employee.paid_monthly_leaves += monthly_leaves
            except:
                employee.unpaid_monthly_leaves += monthly_leaves
            employee.save()
            messages.success(request, f"Leave approved")
            return redirect("/hall/landing")

    else:
        form = LeaveForm()

    return render(
        request,
        "hall_manager/approve_leaves.html",
        context={"form": form, "title": "Leave Approval"},
    )


@permission_required("main.is_hall_manager", "/login")
def make_notice(request):
    if request.method == "POST":
        form = NoticeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            hall_manager = HallManager.objects.filter(client=request.user).first()
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            image = request.FILES["image"]
            obj = Notice(
                title=title,
                content=content,
                hall=hall_manager.hall,
                image=image,
            )
            print(obj)
            obj.save()
            messages.success(request, f"Your notice has been issued.")
            return redirect("/hall/landing")
    else:
        form = NoticeRegistrationForm()

    print(request)
    return render(
        request,
        "hall_manager/make_notice.html",
        context={"form": form, "title": "Notice"},
    )


@permission_required("main.is_hall_manager", "/login")
def hall_landing(request):
    if request.method == "GET":
        hall_manager = HallManager.objects.filter(client=request.user).first()
        notices = Notice.objects.filter(hall=hall_manager.hall)
        print(notices)
        return render(
            request,
            "hall_manager/landing.html",
            context={"notices": notices, "title": "Notices"},
        )


@permission_required("main.is_hall_manager", "/login")
def register_student(request):

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():

            hall = form.cleaned_data.get("hall")

            room_choice1 = form.cleaned_data.get("room_choice1")
            room_choice2 = form.cleaned_data.get("room_choice2")
            room_choice3 = form.cleaned_data.get("room_choice3")

            room1 = Room.objects.filter(code=hall.name + "-" + room_choice1).first()
            room2 = Room.objects.filter(code=hall.name + "-" + room_choice2).first()
            room3 = Room.objects.filter(code=hall.name + "-" + room_choice3).first()
            if room1 == None or room2 == None or room3 == None:
                messages.error(
                    request,
                    "Invalid Room Number",
                )
                return redirect("/hall/register-student")

            stakeholderID = form.cleaned_data.get("stakeholderID")
            email = form.cleaned_data.get("email")
            address = form.cleaned_data.get("address")
            mobile = form.cleaned_data.get("mobile")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
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

            if room1.current_occupancy < room1.sharing:
                room = room1
                room1.current_occupancy = room1.current_occupancy + 1

                if room1.current_occupancy == room1.sharing:
                    room1.is_free = False
                room1.save()

            elif room2.current_occupancy < room2.sharing:
                room = room2
                room2.current_occupancy = room2.current_occupancy + 1
                if room2.current_occupancy == room2.sharing:
                    room2.is_free = False
                room2.save()

            elif room3.current_occupancy < room3.sharing:
                room = room3
                room3.current_occupancy = room3.current_occupancy + 1
                if room3.current_occupancy == room3.sharing:
                    room3.is_free = False
                room3.save()
            else:
                room = Room.objects.filter(is_free=True).first()
                room.current_occupancy = room.current_occupancy + 1
                if room.current_occupancy == room.sharing:
                    room.is_free = False
                room.save()
            perm = Permission.objects.get(name="is_student")
            client.user_permissions.add(perm)
            perm = Permission.objects.get(name="is_menu")
            client.user_permissions.add(perm)
            student = Student(client=client, hall=hall, room=room)
            student.save()
            subject = "Your account needs to be verified"
            message = f"Hi, click on this link to verify your account http://127.0.0.1:8000/hall/verify-student/{token}"
            email_from = "se.mhc.2024@gmail.com"
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request,
                f"Pls click on the link sent to {email} to complete registration",
            )
            return redirect("/hall/landing")

    else:
        form = StudentRegistrationForm()
    return render(
        request,
        "hall_manager/register_student.html",
        context={"form": form, "title": "register"},
    )


@permission_required("main.is_hall_manager", "/login")
def delete_student(request):
    if request.method == "POST":
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            stakeholderID = form.cleaned_data.get("stakeholderID")
            password_to_confirm = form.cleaned_data.get("verify_password")
            client = Client.objects.filter(stakeholderID=stakeholderID).first()
            if client is not None and client.role == "student" and client.is_active:
                student = Student.objects.filter(client=client).first()
                success = request.user.check_password(password_to_confirm)
                if success:
                    room = student.room
                    room.current_occupancy -= 1
                    if room.current_occupancy < room.sharing:
                        room.is_free = True
                    room.save()
                    student.client.delete()
                    messages.success(
                        request,
                        f"Student with stakeholder ID {stakeholderID} has been deleted",
                    )
                else:
                    messages.error(request, "Invalid password")
            else:
                messages.error(request, "Student not found or not verified")
    else:
        form = DeleteUserForm()
    return render(
        request,
        "hall_manager/delete_student.html",
        context={"form": form, "title": "verify"},
    )


@permission_required("main.is_hall_manager", "/login")
def delete_employee(request):
    if request.method == "POST":
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            stakeholderID = form.cleaned_data.get("stakeholderID")
            password_to_confirm = form.cleaned_data.get("verify_password")
            client = Client.objects.filter(stakeholderID=stakeholderID).first()
            print(client.role)
            if client.role == "hall_employee":
                employee = HallEmployee.objects.filter(client=client).first()
                if employee:
                    success = request.user.check_password(password_to_confirm)
                    if success:
                        employee.client.delete()
                        messages.success(
                            request,
                            f"Employee with stakeholder ID {stakeholderID} has been deleted",
                        )
                    else:
                        messages.error(request, "Invalid password")
                else:
                    messages.error(request, "Employee not found or not verified")
    else:
        form = DeleteUserForm()
    return render(
        request,
        "hall_manager/delete_employee.html",
        context={"form": form, "title": "verify"},
    )


@permission_required("main.is_hall_manager", "/login")
def hall_change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            client = request.user
            hall_manager = HallManager.objects.filter(client=client).first()
            current_password = form.cleaned_data.get("current_password")
            success = client.check_password(current_password)
            if success:
                new_password = form.cleaned_data.get("new_password")
                confirm_password = form.cleaned_data.get("confirm_password")
                if new_password == confirm_password:
                    client.set_password(new_password)
                    client.save()
                    hall_manager.client = client
                    hall_manager.save()
                    logout(request)
                    hall_manager = authenticate(
                        request, username=client.stakeholderID, password=new_password
                    )
                    login(request, hall_manager)
                    messages.success(request, f"password has been updated")
                    return redirect("/hall/profile")
                else:
                    messages.error(
                        request, f"New password did not match confirm password"
                    )
                    return redirect("/hall/change-password")
            else:
                messages.error(request, f"Current password entered is incorrect")
                return redirect("/hall/change-password")

    else:
        form = ChangePasswordForm()
    return render(
        request,
        "hall_manager/change_password.html",
        context={"form": form, "title": "Password"},
    )


def verify_student(request, token):
    client = Client.objects.filter(token=token).first()
    student = Student.objects.filter(client=client)[0]
    if client:
        client.is_active = True
        client.save()
        passbook = StudentPassbook(student=student)
        passbook.save()
        messages.info(
            request,
            f"Your account has been verified. Alloted room is {list(student.room.code.split('-'))[1]}",
        )
        return redirect("/hall/landing")
    else:
        return redirect("/error")


@permission_required("main.is_warden", "/login")
@permission_required("main.is_hall_manager", "/login")
def generate_hall_passbook_pdf(request):

    print(request.user)

    try:
        hall_manager = HallManager.objects.filter(client=request.user).first()
        hall = hall_manager.hall
    except:
        warden = Warden.objects.filter(client=request.user).first()
        hall = warden.hall

    hall_passbook = HallPassbook.objects.filter(hall=hall).first()
    transactions_qset = HallTransaction.objects.filter(hall_passbook=hall_passbook)
    transactions = list(transactions_qset.all())

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Hall-Passbook.pdf"'

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
