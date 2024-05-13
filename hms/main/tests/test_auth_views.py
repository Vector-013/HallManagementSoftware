from django.test import TestCase
from ..models import *
from ..forms import *
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta, date
import pytz
from django.contrib.auth.forms import AuthenticationForm


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


class AuthViewsTesting(TestCase):
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
        build_rooms(self.hall)
        self.hall.save()
        self.hall.max_occupancy = self.hall.calculate_max_occupancy()
        self.hall.save()

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
        # perm = Permission.objects.get(name="is_hall_manager")
        # perm2 = Permission.objects.get(name="is_hall")
        # self.person.user_permissions.add(perm)
        # self.person.user_permissions.add(perm2)
        self.person.is_active = True
        self.person.save()

        self.hall_manager = HallManager.objects.create(
            client=self.person, hall=self.hall
        )
        self.hall_manager.save()

        self.sclient12 = Client.objects.create_user(
            stakeholderID="22cs30051",
            email="ojasdubey1@gmail.com",
            password="Test@123",
            mobile="+91 9234567891",
            first_name="Test",
            last_name="1",
            address="Bhopal",
            token="",
            role="student",
        )
        self.sclient12.is_active = True
        # perm = Permission.objects.get(name="is_student")
        # self.sclient12.user_permissions.add(perm)
        self.sclient12.save()
        room1 = Room.objects.filter(hall=self.hall).filter(is_free=True).first()
        room1.current_occupancy += 1
        if room1.current_occupancy == room1.sharing:
            room1.is_free = False
        room1.save()
        self.student12 = Student.objects.create(
            client=self.sclient12, hall=self.hall, room=room1
        )
        self.student12.save()

        self.wperson = Client.objects.create_user(
            stakeholderID="22cs30065",
            email="shreya.bose.in@gmail.com",
            password="Test@123",
            mobile="+91 9234567890",
            first_name="Shreya",
            last_name="Bose",
            address="Bhopal",
            token="",
            role="warden",
        )
        # perm = Permission.objects.get(name="is_warden")
        # perm2 = Permission.objects.get(name="is_hall")
        # self.wperson.user_permissions.add(perm)
        # self.wperson.user_permissions.add(perm2)
        self.wperson.is_active = True
        self.wperson.save()
        self.warden = Warden.objects.create(client=self.wperson, hall=self.hall)

        self.hmcclient = Client.objects.create_user(
            stakeholderID="22cs30066",
            email="ojasdubey13@gmail.com",
            password="Test@123",
            mobile="+91 9234567891",
            first_name="Test",
            last_name="4",
            address="Bhopal",
            token="",
            role="hmc_chairman",
        )

        self.hmcclient.is_active = True
        # perm = Permission.objects.get(name="is_HMC")
        # self.hmcclient.user_permissions.add(perm)
        self.hmcclient.save()
        self.hmc = HMC.objects.create(client=self.hmcclient)

        self.mess_manager_client = Client.objects.create_user(
            stakeholderID="22cs30067",
            email="ojasdubey13@gmail.com",
            password="Test@123",
            mobile="+91 9234567892",
            first_name="Test",
            last_name="4",
            address="Bhopal",
            token="",
            role="mess_manager",
        )
        self.mess_manager_client.is_active = True
        # perm = Permission.objects.get(name="is_mess_manager")
        # self.mess_manager_client.user_permissions.add(perm)
        self.mess_manager_client.save()

        self.mess_manager = MessManager(client=self.mess_manager_client, hall=self.hall)

    def test_login_get(self):
        response = self.client.get(reverse("login"))
        form = response.context["form"]
        self.assertTemplateUsed(response, "auth/login.html")
        self.assertIsInstance(form, AuthenticationForm)

    def test_login_student(self):
        self.client.login(username="22cs30051", password="Test@123")
        url = reverse("login")
        form = AuthenticationForm(
            data={"username": "22cs30051", "password": "Test@123"}
        )
        response = self.client.post(url, data=form.data)

        self.assertRedirects(
            response, "/student/notice", status_code=302, target_status_code=302
        )

    def test_login_hall(self):
        url = reverse("login")
        form = AuthenticationForm(
            data={"username": "22cs30060", "password": "Test@123"}
        )
        response = self.client.post(url, data=form.data)

        self.assertRedirects(
            response, "/hall/landing", status_code=302, target_status_code=302
        )

    def test_login_warden(self):
        url = reverse("login")
        form = AuthenticationForm(
            data={"username": "22cs30065", "password": "Test@123"}
        )
        response = self.client.post(url, data=form.data)

        self.assertRedirects(
            response, "/warden/landing", status_code=302, target_status_code=302
        )

    def test_login_hmc(self):
        url = reverse("login")
        form = AuthenticationForm(
            data={"username": "22cs30066", "password": "Test@123"}
        )
        response = self.client.post(url, data=form.data)

        self.assertRedirects(
            response, "/hmc/landing", status_code=302, target_status_code=302
        )

    def test_login_mess(self):
        url = reverse("login")
        form = AuthenticationForm(
            data={"username": "22cs30067", "password": "Test@123"}
        )
        response = self.client.post(url, data=form.data)

        self.assertRedirects(
            response, "/mess/landing", status_code=302, target_status_code=302
        )

    def test_login_exception(self):
        url = reverse("login")
        form = AuthenticationForm(
            data={"username": "22cs30069", "password": "Test@123"}
        )
        response = self.client.post(url, data=form.data)

        self.assertTemplateUsed(response, "auth/login.html")

    def test_logout(self):
        self.client.login(username="22cs30051", password="Test@123")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(
            response, "/login", status_code=302, target_status_code=301
        )

    def test_get_email(self):
        response = self.client.get(reverse("get_email"))
        form = response.context["form"]
        self.assertIsInstance(form, SendMailForm)
        self.assertTemplateUsed(response, "auth/get_email.html")

    def test_get_email_post(self):
        url = reverse("get_email")
        form = SendMailForm(data={"stakeholderID": "22cs30051"})
        response = self.client.post(url, data=form.data)
        self.assertRedirects(
            response, "/login", status_code=302, target_status_code=301
        )

    def test_get_email_post_exception(self):
        url = reverse("get_email")
        form = SendMailForm(data={"stakeholderID": "22cs30011"})
        response = self.client.post(url, data=form.data)
        self.assertTemplateUsed(response, "auth/get_email.html")

    def test_password_forgot(self):
        response = self.client.get(reverse("forgot_password", args=["22cs30051"]))
        self.assertTemplateUsed(response, "auth/forgot_password.html")

    def test_password_forgot_post(self):
        url = reverse("forgot_password", args=["22cs30051"])
        form = ForgotPasswordForm(
            data={"new_password": "Test@1234", "confirm_password": "Test@1234"}
        )
        response = self.client.post(url, data=form.data)
        self.assertEqual(
            self.client.login(username="22cs30051", password="Test@1234"), True
        )
        self.assertRedirects(
            response, "/login", status_code=302, target_status_code=301
        )

    def test_password_forgot_post_exception(self):
        url = reverse("forgot_password", args=["22cs30051"])
        form = ForgotPasswordForm(
            data={"new_password": "Test@1234", "confirm_password": "Test@124"}
        )
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, url, status_code=302, target_status_code=200)

    def test_entry(self):
        response = self.client.get(reverse("entry"))
        self.assertRedirects(
            response, "/login", status_code=302, target_status_code=301
        )
