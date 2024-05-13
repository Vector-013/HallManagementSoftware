from django.test import TestCase
from ..models import *
from ..forms import *
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
import pytz


class StudentViewTesting(TestCase):

    def setUp(self):
        self.hall = Hall.objects.create(
            name="Hall1",
            max_occupancy=100,
            blocks=1,
            floors=2,
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
            role="student",
        )
        perm = Permission.objects.get(name="is_student")
        self.person.user_permissions.add(perm)
        self.person.is_active = True
        self.person.save()
        room = Room.objects.create(
            hall=self.hall,
            code="A101",
            sharing=1,
            current_occupancy=1,
        )
        self.student = Student.objects.create(
            client=self.person,
            hall=self.hall,
            room=room,
        )

        self.sudent_passbook = StudentPassbook.objects.create(
            student=self.student,
        )
        self.due1 = Due.objects.create(
            demand=1000,
            type="Mess Dues",
            student_passbook=self.sudent_passbook,
        )
        self.due2 = Due.objects.create(
            demand=1090,
            type="Hall Dues",
            student_passbook=self.sudent_passbook,
        )
        self.payment1 = StudentPayment.objects.create(
            student_passbook=self.sudent_passbook
        )
        self.student_complaint1 = Complaint.objects.create(
            title="Test Complaint",
            content="Test Complaint Description",
            student=self.student,
            hall=self.hall,
            category="room condition",
        )
        self.student_complaint2 = Complaint.objects.create(
            title="Test Complaint 2",
            content="Test Complaint Description 2",
            student=self.student,
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

        self.person2 = Client.objects.create_user(
            stakeholderID="22cs30061",
            email="shreya.bose.in@gmail.com",
            password="Test@123",
            mobile="+91 9234567890",
            first_name="Shreya",
            last_name="Bose",
            address="Bhopal",
            token="",
            role="hall_employee",
        )
        self.hall_employee = HallEmployee.objects.create(
            client=self.person2,
            hall=self.hall,
            role="cook",
            salary=10000,
        )
        self.complaint1_atr = ATR.objects.create(
            complaint=self.student_complaint1,
            employee=self.hall_employee,
            report="done",
        )

    def test_student_view_profile(self):
        self.client.login(username="22cs30060", password="Test@123")
        student = Student.objects.filter(client=self.person).first()
        self.assertEqual(student.__str__(), "Ojas Dubey")
        url = reverse("student_view_profile")
        self.assertEquals(url, "/student/profile")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "student/profile.html")

    def test_student_change_password(self):
        self.client.login(username="22cs30060", password="Test@123")
        student = Student.objects.filter(client=self.person).first()

        form = ChangePasswordForm(
            data={
                "current_password": "Test@123",
                "new_password": "Test@1234",
                "confirm_password": "Test@1234",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data.get("current_password") == "Test@123")
        self.assertTrue(
            form.cleaned_data.get("new_password")
            == form.cleaned_data.get("confirm_password")
        )
        url = reverse("student_change_password")
        self.assertEquals(url, "/student/change-password/")
        response = self.client.post(url, data=form.data)
        self.person.set_password("Test@1234")
        self.client.logout()
        self.client.login(username="22cs30060", password="Test@1234")
        self.assertRedirects(response, "/student/profile")

        self.client.logout()
        self.assertFalse(self.client.login(username="22cs30060", password="Test@123"))
        self.assertTrue(self.client.login(username="22cs30060", password="Test@1234"))

    def test_student_change_password_invalid(self):
        self.client.login(username="22cs30060", password="Test@123")
        form = ChangePasswordForm(
            data={
                "current_password": "Test@123",
                "new_password": "Test@12346",
                "confirm_password": "Test@12345",
            }
        )
        url = reverse("student_change_password")
        self.assertEquals(url, "/student/change-password/")
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data=form.data)

        self.assertRedirects(
            response,
            "/student/change-password",
            status_code=302,
            target_status_code=301,
        )

    def test_student_change_password_invalid_current_password(self):
        self.client.login(username="22cs30060", password="Test@123")
        form = ChangePasswordForm(
            data={
                "current_password": "Test@1234",
                "new_password": "Test@12346",
                "confirm_password": "Test@12346",
            }
        )
        url = reverse("student_change_password")
        self.assertEquals(url, "/student/change-password/")
        self.assertTrue(form.is_valid())

        response = self.client.post(url, data=form.data)

        self.assertRedirects(
            response,
            "/student/change-password",
            status_code=302,
            target_status_code=301,
        )

    def test_student_change_password_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("student_change_password")
        self.assertEquals(url, "/student/change-password/")
        response = self.client.get(url)
        form = response.context.get("form")
        self.assertIsInstance(form, ChangePasswordForm)
        self.assertTemplateUsed(response, "student/change_password.html")

    def test_make_complaints_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("make_complaints")
        self.assertEquals(url, "/student/make-complaints/")
        response = self.client.get(url)
        form = response.context.get("form")
        self.assertIsInstance(form, ComplaintRegistrationForm)
        self.assertTemplateUsed(response, "student/make_complaints.html")

    def test_make_complaints_post(self):
        self.client.login(username="22cs30060", password="Test@123")
        student = Student.objects.filter(client=self.person).first()
        url = reverse("make_complaints")
        self.assertEquals(url, "/student/make-complaints/")
        smol_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded = SimpleUploadedFile("small.gif", smol_gif, content_type="image/gif")
        form = ComplaintRegistrationForm(
            data={
                "title": "Test Complaint",
                "content": "Test Complaint Description",
                "category": "room condition",
                "image": uploaded,
            }
        )
        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(
            response,
            "/student/view-complaints",
            status_code=302,
            target_status_code=301,
        )

    def test_view_complaints_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("view_complaints")
        self.assertEquals(url, "/student/view-complaints/")
        response = self.client.get(url)
        complaints = response.context.get("complaints")
        self.assertTrue(
            complaints == [self.student_complaint1, self.student_complaint2]
        )
        self.assertTemplateUsed(response, "student/view_complaints.html")

    def test_notice_student_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("student_notice")
        self.assertEquals(url, "/student/notice")
        response = self.client.get(url)
        notices = response.context.get("notices")
        self.assertTrue(list(notices) == [self.hall_notice1, self.hall_notice2])
        self.assertTemplateUsed(response, "student/view_notice.html")

    def test_generate_atr_pdf(self):
        complaint = self.student_complaint1
        pk = complaint.pk
        url = reverse("atr_pdf", args=[pk])
        self.assertEquals(url, f"/student/generate-atr-pdf/{pk}")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_generate_student_passbook_pdf(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("student_passbook_pdf")
        self.assertEquals(url, "/student/generate-passbook-pdf")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
