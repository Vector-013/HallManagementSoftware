from django.test import TestCase
from ..models import *
from ..forms import *
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta, date
import pytz


def build_rooms(hall):
    for x in range(int(hall.blocks)):
        for y in range(int(hall.floors)):
            for z in range(int(hall.singles)):
                room = Room(
                    hall=hall,
                    rent=9,
                    sharing=1,
                    floor=y,
                    block=chr(65 + x),
                    number=z,
                    code=hall.name + "-" + str(chr(65 + x)) + str(y) + str(z),
                )
                room.save()

    x = 0
    y = 0

    for x in range(int(hall.blocks)):
        for y in range(int(hall.floors)):
            for z in range(int(hall.singles), int(hall.singles) + int(hall.doubles)):
                room = Room(
                    hall=hall,
                    rent=1,
                    sharing=2,
                    floor=y,
                    block=chr(65 + x),
                    number=z,
                    code=hall.name + "-" + str(chr(65 + x)) + str(y) + str(z),
                )
                room.save()

    x = 0
    y = 0

    for x in range(int(hall.blocks)):
        for y in range(int(hall.floors)):
            for z in range(
                int(hall.singles) + int(hall.doubles),
                int(hall.singles) + int(hall.doubles) + int(hall.triples),
            ):
                room = Room(
                    hall=hall,
                    rent=0,
                    sharing=3,
                    floor=y,
                    block=chr(65 + x),
                    number=z,
                    code=hall.name + "-" + str(chr(65 + x)) + str(y) + str(z),
                )
                room.save()


class HallManagerViewTesting(TestCase):
    def setUp(self):
        self.hall = Hall.objects.create(
            name="Hall1",
            max_occupancy=100,
            blocks=2,
            floors=3,
            singles=10,
            doubles=10,
            triples=10,
        )
        self.person = Client.objects.create_user(
            stakeholderID="22cs30060",
            email="ojasdubey13@gmail.com",
            password="Test@123",
            mobile="+91 9234567890",
            first_name="Ojas",
            last_name="Dubey",
            address="Bhopal",
            token="",
            role="hall_manager",
        )
        perm = Permission.objects.get(name="is_hall_manager")
        perm2 = Permission.objects.get(name="is_hall")
        self.person.user_permissions.add(perm)
        self.person.user_permissions.add(perm2)
        self.person.is_active = True
        self.person.save()

        self.hall_manager = HallManager.objects.create(
            client=self.person, hall=self.hall
        )

        build_rooms(self.hall)
        self.hall.save()
        self.hall.max_occupancy = self.hall.calculate_max_occupancy()
        self.hall.save()

        self.sclient1 = Client.objects.create_user(
            stakeholderID="22cs30061",
            email="test1@gmail.com",
            password="Test@123",
            mobile="+91 9234567891",
            first_name="Test",
            last_name="1",
            address="Bhopal",
            token="",
            role="student",
        )
        self.sclient1.is_active = True
        self.sclient1.save()
        room1 = Room.objects.filter(hall=self.hall).filter(is_free=True).first()
        room1.current_occupancy += 1
        if room1.current_occupancy == room1.sharing:
            room1.is_free = False
        room1.save()
        self.student1 = Student.objects.create(
            client=self.sclient1, hall=self.hall, room=room1
        )
        self.student1.save()

        self.sclient2 = Client.objects.create_user(
            stakeholderID="22cs30062",
            email="test2@gmail.com",
            password="Test@123",
            mobile="+91 9234567892",
            first_name="Test",
            last_name="2",
            address="Bhopal",
            token="",
            role="student",
        )
        self.sclient2.is_active = True
        self.sclient2.save()
        room2 = (
            Room.objects.filter(hall=self.hall)
            .filter(is_free=True)
            .filter(sharing=2)
            .first()
        )
        room2.current_occupancy += 1
        if room2.current_occupancy == room2.sharing:
            room2.is_free = False
        room2.save()
        self.student2 = Student.objects.create(
            client=self.sclient2, hall=self.hall, room=room2
        )
        self.student2.save()

        self.sclient3 = Client.objects.create_user(
            stakeholderID="22cs30063",
            email="test3@gmail.com",
            password="Test@123",
            mobile="+91 9234567893",
            first_name="Test",
            last_name="3",
            address="Bhopal",
            token="",
            role="student",
        )
        self.sclient3.is_active = True
        self.sclient3.save()
        room3 = Room.objects.filter(hall=self.hall).filter(is_free=True).first()
        room3.current_occupancy += 1
        if room3.current_occupancy == room3.sharing:
            room3.is_free = False
        room3.save()
        self.student3 = Student.objects.create(
            client=self.sclient3, hall=self.hall, room=room3
        )
        self.student3.save()

        self.sclient4 = Client.objects.create_user(
            stakeholderID="22cs30064",
            email="test4@gmail.com",
            password="Test@123",
            mobile="+91 9234567894",
            first_name="Test",
            last_name="4",
            address="Bhopal",
            token="testtoken123",
            role="student",
        )
        self.sclient4.is_active = True
        self.sclient4.save()
        room4 = Room.objects.filter(hall=self.hall).filter(is_free=True).first()
        room4.current_occupancy += 1
        if room4.current_occupancy == room4.sharing:
            room4.is_free = False
        room4.save()
        self.student4 = Student.objects.create(
            client=self.sclient4, hall=self.hall, room=room4
        )
        self.student4.save()

        self.wperson = Client.objects.create_user(
            stakeholderID="22cs30065",
            email="shreya.bose.in@gmail.com",
            password="Test@123",
            mobile="+91 9234567890",
            first_name="Shreya",
            last_name="Bose",
            address="Bhopal",
            token="",
            role="hall_manager",
        )
        perm = Permission.objects.get(name="is_warden")
        perm2 = Permission.objects.get(name="is_hall")
        self.wperson.user_permissions.add(perm)
        self.wperson.user_permissions.add(perm2)
        self.wperson.is_active = True
        self.wperson.save()
        self.warden = Warden.objects.create(client=self.wperson, hall=self.hall)

        self.cemployee1 = Client.objects.create_user(
            stakeholderID="22cs30066",
            email="test6@gmail.com",
            password="Test@123",
            mobile="+91 9234567896",
            first_name="EmpTest1",
            last_name="6",
            address="Bhopal",
            token="",
            role="hall_employee",
        )
        self.cemployee1.is_active = True
        self.cemployee1.save()
        self.employee1 = HallEmployee.objects.create(
            client=self.cemployee1, hall=self.hall
        )
        self.employee1.save()
        self.cemployee2 = Client.objects.create_user(
            stakeholderID="22cs30067",
            email="test7@gmail.com",
            password="Test@123",
            mobile="+91 9234567897",
            first_name="Test",
            last_name="7",
            address="Bhopal",
            token="",
            role="hall_employee",
        )
        self.cemployee2.save()
        self.employee2 = HallEmployee.objects.create(
            client=self.cemployee2, hall=self.hall, role="gardener"
        )
        self.employee2.save()

        self.student_complaint1 = Complaint.objects.create(
            title="Test Complaint",
            content="Test Complaint Description",
            student=self.student1,
            hall=self.hall,
            category="room condition",
        )
        self.student_complaint2 = Complaint.objects.create(
            title="Test Complaint 2",
            content="Test Complaint Description 2",
            student=self.student2,
            hall=self.hall,
            category="room condition",
            status=True,
        )
        self.hall_notice1 = Notice.objects.create(
            title="Test Notice1",
            content="Test Notice Description1",
            date_created=datetime.now(pytz.timezone("Asia/Kolkata")),
            hall=self.hall,
        )
        self.hall_notice2 = Notice.objects.create(
            title="Test Notice2",
            content="Test Notice Description2",
            date_created=datetime.now(pytz.timezone("Asia/Kolkata")),
            hall=self.hall,
        )
        self.hall_passbook = HallPassbook.objects.create(hall=self.hall)
        self.transaction = HallTransaction.objects.create(
            type="Salaries",
            amount=1000,
            hall_passbook=self.hall_passbook,
            timestamp=datetime.now(pytz.timezone("Asia/Kolkata")),
        )

    def test_manager_hall_occupancy(self):
        self.client.login(username="22cs30060", password="Test@123")
        response = self.client.get(reverse("view_hall_occupancy"))
        self.assertTemplateUsed(response, "hall_manager/hall_occupancy.html")
        self.assertEqual(response.context["hall"], self.hall)
        self.assertEqual(response.context["total_occupied"], 4)
        self.assertEqual(response.context["total_capacity"], self.hall.max_occupancy)

    def test_warden_hall_occupancy(self):
        self.client.login(username="22cs30065", password="Test@123")
        response = self.client.get(reverse("view_hall_occupancy"))
        self.assertTemplateUsed(response, "hall_manager/hall_occupancy.html")
        self.assertEqual(response.context["hall"], self.hall)
        self.assertEqual(response.context["total_occupied"], 4)
        self.assertEqual(response.context["total_capacity"], self.hall.max_occupancy)

    def test_manager_view_students(self):
        self.client.login(username="22cs30060", password="Test@123")
        response = self.client.get(reverse("view_student_details"))
        self.assertTemplateUsed(response, "hall_manager/view_students.html")
        self.assertEqual(len(response.context["students"]), 4)
        self.assertNotEqual(len(response.context["students"]), 0)

    def test_warden_view_students(self):
        self.client.login(username="22cs30065", password="Test@123")
        response = self.client.get(reverse("view_student_details"))
        self.assertTemplateUsed(response, "hall_manager/view_students.html")
        self.assertEqual(len(response.context["students"]), 4)
        self.assertNotEqual(len(response.context["students"]), 0)

    def test_manager_view_employees(self):
        self.client.login(username="22cs30060", password="Test@123")
        response = self.client.get(reverse("view_employee_details"))
        self.assertTemplateUsed(response, "hall_manager/view_employees.html")
        self.assertEqual(len(response.context["employees"]), 2)
        self.assertNotEqual(len(response.context["employees"]), 0)
        self.assertEqual(response.context["employees"][0].role, "mess_worker")
        self.assertEqual(response.context["employees"][1].role, "gardener")
        self.assertEqual(response.context["employees"][0].client, self.cemployee1)

    def test_warden_view_employees(self):
        self.client.login(username="22cs30065", password="Test@123")
        response = self.client.get(reverse("view_employee_details"))
        self.assertTemplateUsed(response, "hall_manager/view_employees.html")
        self.assertEqual(len(response.context["employees"]), 2)
        self.assertNotEqual(len(response.context["employees"]), 0)
        self.assertEqual(response.context["employees"][0].role, "mess_worker")
        self.assertEqual(response.context["employees"][1].role, "gardener")
        self.assertEqual(response.context["employees"][0].client, self.cemployee1)

    def test_hall_view_profile(self):
        self.client.login(username="22cs30060", password="Test@123")
        response = self.client.get(reverse("hall_view_profile"))
        self.assertTemplateUsed(response, "hall_manager/profile.html")
        self.assertEqual(response.context["hall_manager"], self.hall_manager)

    def test_warden_hall_view_profile(self):
        self.client.login(username="22cs30065", password="Test@123")
        response = self.client.get(reverse("hall_view_profile"))
        self.assertTemplateUsed(response, "hall_manager/profile.html")
        self.assertEqual(response.context["hall_manager"], self.hall_manager)

    def test_update_view_profile(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("update_student_profile", args=[self.sclient1.stakeholderID])
        student = Student.objects.get(client=self.sclient1)

        form = UpdateStudentForm(
            data={
                "email": "test1@gmail.com",
                "mobile": "+91 9234567891",
                "first_name": "Test_one",
                "last_name": "1",
                "address": "Delhi",
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)

        self.assertEqual(student.client.first_name, "Test_one")
        self.assertEqual(student.client.last_name, "1")
        self.assertEqual(student.client.email, "test1@gmail.com")
        self.assertEqual(student.client.mobile, "+91 9234567891")
        self.assertEqual(student.client.address, "Delhi")

        self.assertRedirects(response, reverse("search_student"))

    def test_update_view_profile_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("update_student_profile", args=[self.sclient1.stakeholderID])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/update_student_profile.html")
        form = response.context["form"]
        self.assertIsInstance(form, UpdateStudentForm)

    def test_update_employee_profile(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("update_employee_profile", args=[self.cemployee1.stakeholderID])
        employee = HallEmployee.objects.get(client=self.cemployee1)

        form = UpdateEmployeeForm(
            data={
                "email": "test6@gmail.com",
                "address": "Delhi",
                "mobile": "+91 9234567896",
                "first_name": "EmpTest100",
                "last_name": "6",
                "hall": self.hall.id,
                "role": "mess_worker",
                "salary": int(10000),
                "unpaid_monthly_leaves": int(0),
                "paid_monthly_leaves": int(0),
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        employee.refresh_from_db()

        self.assertEqual(employee.client.first_name, "EmpTest100")
        self.assertEqual(employee.client.last_name, "6")
        self.assertEqual(employee.client.email, "test6@gmail.com")
        self.assertEqual(employee.client.mobile, "+91 9234567896")
        self.assertEqual(employee.client.address, "Delhi")
        self.assertEqual(employee.hall, self.hall)
        self.assertEqual(employee.salary, 10000)
        self.assertEqual(employee.role, "mess_worker")

        self.assertRedirects(response, reverse("search_employee"))

    def test_update_employee_profile_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("update_employee_profile", args=[self.cemployee1.stakeholderID])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/update_student_profile.html")
        form = response.context["form"]
        self.assertIsInstance(form, UpdateEmployeeForm)

    def test_search_user_student(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("search_student")
        student = Student.objects.get(client=self.sclient1)
        form = UserSearchForm(data={"stakeholderID": "22cs30061"})
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/hall/update-student-profile/22cs30061")

    def test_search_user_employee(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("search_employee")
        employee = HallEmployee.objects.get(client=self.cemployee1)
        form = UserSearchForm(data={"stakeholderID": "22cs30066"})
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/hall/update-employee-profile/22cs30066")

    def test_search_user_student_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("search_student")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/search_user.html")
        form = response.context["form"]
        self.assertIsInstance(form, UserSearchForm)

    def test_search_user_exception(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("search_student")
        form = UserSearchForm(data={"stakeholderID": "22cs30058"})
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/hall/search-student")

    def test_search_user_warden(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("search_student")
        form = UserSearchForm(data={"stakeholderID": "22cs30065"})
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/hall/search-student")

    def test_create_atr(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("create_atr")
        form = ATRForm(
            data={
                "complaint": self.student_complaint1.id,
                "employee": self.employee1.client.id,
                "report": "Test ATR report",
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/hall/complaints")

    def test_create_atr_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("create_atr")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/create_atr.html")
        form = response.context["form"]
        self.assertIsInstance(form, ATRForm)

    def test_hall_complaints(self):
        self.client.login(username="22cs30060", password="Test@123")
        response = self.client.get(reverse("hall_complaints"))
        self.assertTemplateUsed(response, "hall_manager/complaints.html")
        self.assertEqual(len(response.context["complaints"]), 2)
        self.assertNotEqual(len(response.context["complaints"]), 0)

    def test_hall_warden_complaints(self):
        self.client.login(username="22cs30065", password="Test@123")
        response = self.client.get(reverse("hall_complaints"))
        self.assertTemplateUsed(response, "hall_manager/complaints.html")
        self.assertEqual(len(response.context["complaints"]), 2)
        self.assertNotEqual(len(response.context["complaints"]), 0)

    def test_add_employee(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("add_employee")

        form = WorkerRegistrationForm(
            data={
                "stakeholderID": "22cs30068",
                "email": "test8@gmail.com",
                "address": "Delhi",
                "mobile": "+91 9234567898",
                "first_name": "EmpTest2",
                "last_name": "8",
                "role": "mess_worker",
                "salary": int(10000),
            }
        )

        self.assertEqual(form.is_valid(), True)
        response = self.client.post(url, data=form.data)
        new_employee = HallEmployee.objects.get(client__stakeholderID="22cs30068")
        self.assertEqual(new_employee.client.first_name, "EmpTest2")
        self.assertEqual(new_employee.client.last_name, "8")
        self.assertEqual(new_employee.client.email, "test8@gmail.com")
        self.assertEqual(new_employee.client.mobile, "+91 9234567898")
        self.assertEqual(new_employee.client.address, "Delhi")
        self.assertEqual(new_employee.role, "mess_worker")
        self.assertEqual(new_employee.salary, 10000)
        self.assertRedirects(response, "/hall/landing")

    def test_add_employee_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("add_employee")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/add_employee.html")
        form = response.context["form"]
        self.assertIsInstance(form, WorkerRegistrationForm)

    def test_approve_leaves(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("approve_leaves")
        smol_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded = SimpleUploadedFile("small.gif", smol_gif, content_type="image/gif")
        form = LeaveForm(
            data={
                "stakeholderID": self.employee1.client.stakeholderID,
                "start_date": date(2024, 1, 1),
                "end_date": date(2024, 1, 5),
                "uploads": uploaded,
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.employee1.refresh_from_db()
        self.assertEqual(self.employee1.unpaid_monthly_leaves, 0)
        self.assertEqual(self.employee1.paid_monthly_leaves, 4)
        self.assertRedirects(response, "/hall/landing")

    def test_approve_leaves_without_upload(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("approve_leaves")
        smol_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded = SimpleUploadedFile("small.gif", smol_gif, content_type="image/gif")
        form = LeaveForm(
            data={
                "stakeholderID": self.employee1.client.stakeholderID,
                "start_date": date(2024, 1, 1),
                "end_date": date(2024, 1, 5),
                "uploads": "",
            }
        )
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data=form.data)
        self.employee1.refresh_from_db()
        self.assertEqual(self.employee1.unpaid_monthly_leaves, 4)
        self.assertEqual(self.employee1.paid_monthly_leaves, 0)
        self.assertRedirects(response, "/hall/landing")

    def test_approve_leaves_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("approve_leaves")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/approve_leaves.html")
        form = response.context["form"]
        self.assertIsInstance(form, LeaveForm)

    def test_make_notice(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("make_notice")
        smol_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded = SimpleUploadedFile("small.gif", smol_gif, content_type="image/gif")
        form = NoticeRegistrationForm(
            data={
                "title": "Test Notice",
                "content": "Test Notice Description",
                "image": uploaded,
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/hall/landing")
        self.assertEqual(Notice.objects.count(), 3)

    def test_make_notice_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("make_notice")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/make_notice.html")
        form = response.context["form"]
        self.assertIsInstance(form, NoticeRegistrationForm)

    def test_register_student(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("register_student")
        form = StudentRegistrationForm(
            data={
                "stakeholderID": "22cs30069",
                "email": "test9@gmail.com",
                "password": "Test@123",
                "address": "Delhi",
                "mobile": "+91 9234567899",
                "first_name": "Test",
                "last_name": "9",
                "hall": self.hall.id,
                "room_choice1": "A00",
                "room_choice2": "A01",
                "room_choice3": "A02",
            }
        )
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data=form.data)
        student_new = Student.objects.get(client__stakeholderID="22cs30069")
        self.assertEqual(Student.objects.count(), 5)
        self.assertEqual(student_new.client.first_name, "Test")
        self.assertEqual(student_new.client.last_name, "9")
        self.assertEqual(student_new.client.email, "test9@gmail.com")
        self.assertEqual(student_new.client.mobile, "+91 9234567899")
        self.assertEqual(student_new.client.address, "Delhi")
        self.assertEqual(student_new.hall, self.hall)
        self.assertRedirects(response, "/hall/landing")

    def test_register_student_exception(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("register_student")
        form = StudentRegistrationForm(
            data={
                "stakeholderID": "22cs30069",
                "email": "test9@gmail.com",
                "password": "Test@123",
                "address": "Delhi",
                "mobile": "+91 9234567899",
                "first_name": "Test",
                "last_name": "9",
                "hall": self.hall.id,
                "room_choice1": "A220",
                "room_choice2": "A131",
                "room_choice3": "A044",
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(
            response, "/hall/register-student", status_code=302, target_status_code=301
        )

    def test_register_student_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("register_student")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/register_student.html")
        form = response.context["form"]
        self.assertIsInstance(form, StudentRegistrationForm)

    def test_register_student_room_conditions(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("register_student")
        form = StudentRegistrationForm(
            data={
                "stakeholderID": "22cs30069",
                "email": "test9@gmail.com",
                "password": "Test@123",
                "address": "Delhi",
                "mobile": "+91 9234567899",
                "first_name": "Test",
                "last_name": "9",
                "hall": self.hall.id,
                "room_choice1": "A010",
                "room_choice2": "A12",
                "room_choice3": "A14",
            }
        )
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data=form.data)
        student_new = Student.objects.get(client__stakeholderID="22cs30069")
        self.assertEqual(Student.objects.count(), 5)
        self.assertEqual(student_new.client.first_name, "Test")
        self.assertEqual(student_new.client.last_name, "9")
        self.assertEqual(student_new.client.email, "test9@gmail.com")
        self.assertEqual(student_new.client.mobile, "+91 9234567899")
        self.assertEqual(student_new.client.address, "Delhi")
        self.assertEqual(student_new.hall, self.hall)
        self.assertRedirects(response, "/hall/landing")

    def test_register_student_room_conditions1(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("register_student")
        form = StudentRegistrationForm(
            data={
                "stakeholderID": "22cs30069",
                "email": "test9@gmail.com",
                "password": "Test@123",
                "address": "Delhi",
                "mobile": "+91 9234567899",
                "first_name": "Test",
                "last_name": "9",
                "hall": self.hall.id,
                "room_choice1": "A06",
                "room_choice2": "A12",
                "room_choice3": "A14",
            }
        )
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data=form.data)
        student_new = Student.objects.get(client__stakeholderID="22cs30069")
        self.assertEqual(Student.objects.count(), 5)
        self.assertEqual(student_new.client.first_name, "Test")
        self.assertEqual(student_new.client.last_name, "9")
        self.assertEqual(student_new.client.email, "test9@gmail.com")
        self.assertEqual(student_new.client.mobile, "+91 9234567899")
        self.assertEqual(student_new.client.address, "Delhi")
        self.assertEqual(student_new.hall, self.hall)
        self.assertRedirects(response, "/hall/landing")

    def test_register_student_room_conditions2(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("register_student")
        form = StudentRegistrationForm(
            data={
                "stakeholderID": "22cs30069",
                "email": "test9@gmail.com",
                "password": "Test@123",
                "address": "Delhi",
                "mobile": "+91 9234567899",
                "first_name": "Test",
                "last_name": "9",
                "hall": self.hall.id,
                "room_choice1": "A00",
                "room_choice2": "A00",
                "room_choice3": "A00",
            }
        )
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data=form.data)
        student_new = Student.objects.get(client__stakeholderID="22cs30069")
        self.assertEqual(Student.objects.count(), 5)
        self.assertEqual(student_new.client.first_name, "Test")
        self.assertEqual(student_new.client.last_name, "9")
        self.assertEqual(student_new.client.email, "test9@gmail.com")
        self.assertEqual(student_new.client.mobile, "+91 9234567899")
        self.assertEqual(student_new.client.address, "Delhi")
        self.assertEqual(student_new.hall, self.hall)
        self.assertRedirects(response, "/hall/landing")

    def test_delete_student(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("delete_student")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30061", "verify_password": "Test@123"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(Student.objects.count(), 3)
        self.assertTemplateUsed(response, "hall_manager/delete_user.html")

    def test_delete_student_exception(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("delete_student")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30061", "verify_password": "Test@1234"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(Student.objects.count(), 4)
        self.assertTemplateUsed(response, "hall_manager/delete_user.html")

    def test_delete_student_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("delete_student")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/delete_user.html")
        form = response.context["form"]
        self.assertIsInstance(form, DeleteUserForm)

    def test_delete_student_fail(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("delete_student")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30021", "verify_password": "Test@123"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(Student.objects.count(), 4)
        self.assertTemplateUsed(response, "hall_manager/delete_user.html")

    def test_delete_employee(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("delete_employee")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30066", "verify_password": "Test@123"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(HallEmployee.objects.count(), 1)
        self.assertTemplateUsed(response, "hall_manager/delete_user.html")

    def test_delete_employee_fail(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("delete_employee")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30021", "verify_password": "Test@123"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(HallEmployee.objects.count(), 2)
        self.assertTemplateUsed(response, "hall_manager/delete_user.html")

    def test_delete_employee_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("delete_employee")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/delete_user.html")
        form = response.context["form"]
        self.assertIsInstance(form, DeleteUserForm)

    def test_delete_employee_exception(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("delete_employee")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30066", "verify_password": "Test@1234"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(HallEmployee.objects.count(), 2)
        self.assertTemplateUsed(response, "hall_manager/delete_user.html")

    def test_hall_change_password(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("hall_change_password")
        form = ChangePasswordForm(
            data={
                "current_password": "Test@123",
                "new_password": "Test@1234",
                "confirm_password": "Test@1234",
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(
            response, "/hall/profile", status_code=302, target_status_code=301
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30060", password="Test@1234"), True
        )

    def test_hall_change_password_fail(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("hall_change_password")
        form = ChangePasswordForm(
            data={
                "current_password": "Test@123",
                "new_password": "Test@1234",
                "confirm_password": "Test@12345",
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(
            response, "/hall/change-password", status_code=302, target_status_code=301
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30060", password="Test@123"), True
        )

    def test_hall_change_password_mismatch(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("hall_change_password")
        form = ChangePasswordForm(
            data={
                "current_password": "Test@1234",
                "new_password": "Test@1234",
                "confirm_password": "Test@12345",
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(
            response, "/hall/change-password", status_code=302, target_status_code=301
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30060", password="Test@123"), True
        )

    def test_hall_change_password_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("hall_change_password")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hall_manager/change_password.html")
        form = response.context["form"]
        self.assertIsInstance(form, ChangePasswordForm)

    def test_verify_student(self):
        url = reverse("verify_student", args=[self.sclient4.token])
        response = self.client.get(url)
        self.assertRedirects(
            response, "/hall/landing", status_code=302, target_status_code=302
        )

    def test_verify_student_fail(self):
        url = reverse("verify_student", args=["testtoken23"])
        response = self.client.get(url)
        self.assertRedirects(response, "/error")

    def test_generate_hall_passbook_manager(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("hall_passbook_pdf")
        self.assertEquals(url, "/hall/generate-passbook-pdf")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_generate_hall_passbook_warden(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("hall_passbook_pdf")
        self.assertEquals(url, "/hall/generate-passbook-pdf")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
