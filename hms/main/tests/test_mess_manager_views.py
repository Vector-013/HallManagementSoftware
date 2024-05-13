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


class MessManagerViewTesting(TestCase):
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
        perm = Permission.objects.get(name="is_mess_manager")
        perm2 = Permission.objects.get(name="is_mess")
        # perm3 = Permission.objects.get(name="is_menu")
        self.person.user_permissions.add(perm)
        self.person.user_permissions.add(perm2)
        # self.person.user_permissions.add(perm3)
        self.person.is_active = True
        self.person.save()

        self.hall_manager = MessManager.objects.create(
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
        # perm3 = Permission.objects.get(name="is_menu")
        # self.sclient1.user_permissions.add(perm3)
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
        perm2 = Permission.objects.get(name="is_mess")
        self.wperson.user_permissions.add(perm)
        self.wperson.user_permissions.add(perm2)
        self.wperson.is_active = True
        self.wperson.save()
        self.warden = Warden.objects.create(client=self.wperson, hall=self.hall)

        self.mess_passbook = MessPassbook.objects.create(hall=self.hall)
        self.transaction = MessTransaction.objects.create(
            type="Salaries",
            amount=1000,
            mess_passbook=self.mess_passbook,
            timestamp=datetime.now(pytz.timezone("Asia/Kolkata")),
        )

        self.menu = Menu.objects.create(hall=self.hall, month="January")

    def test_mess_view_manager_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("mess_view_profile")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "mess_manager/profile.html")
        self.assertEqual(response.context["mess_manager"], self.hall_manager)

    def test_mess_view_warden_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("mess_view_profile")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "mess_manager/profile.html")

    def test_mess_landing(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("mess_landing")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "mess_manager/landing.html")

    def test_mess_change_password(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("mess_change_password")
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
            response, "/mess/profile", status_code=302, target_status_code=301
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30060", password="Test@1234"), True
        )

    def test_mess_change_password_fail(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("mess_change_password")
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
            response, "/mess/change-password", status_code=302, target_status_code=301
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30060", password="Test@123"), True
        )

    def test_mess_change_password_mismatch(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("mess_change_password")
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
            response, "/mess/change-password", status_code=302, target_status_code=301
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30060", password="Test@123"), True
        )

    def test_mess_change_password_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("mess_change_password")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "mess_manager/change_password.html")
        form = response.context["form"]
        self.assertIsInstance(form, ChangePasswordForm)

    def test_make_menu_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("make_menu")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "mess_manager/make_menu.html")
        form = response.context["form"]

    def test_make_menu_post(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("make_menu")

        form = MenuForm(
            data={
                "month": "January",
                "monday_breakfast": "Poha",
                "monday_lunch": "Rice",
                "monday_snacks": "Biscuits",
                "monday_dinner": "Dal",
                "tuesday_breakfast": "Poha",
                "tuesday_lunch": "Rice",
                "tuesday_snacks": "Biscuits",
                "tuesday_dinner": "Dal",
                "wednesday_breakfast": "Poha",
                "wednesday_lunch": "Rice",
                "wednesday_snacks": "Biscuits",
                "wednesday_dinner": "Dal",
                "thursday_breakfast": "Poha",
                "thursday_lunch": "Rice",
                "thursday_snacks": "Biscuits",
                "thursday_dinner": "Dal",
                "friday_breakfast": "Poha",
                "friday_lunch": "Rice",
                "friday_snacks": "Biscuits",
                "friday_dinner": "Dal",
                "saturday_breakfast": "Poha",
                "saturday_lunch": "Rice",
                "saturday_snacks": "Biscuits",
                "saturday_dinner": "Dal",
                "sunday_breakfast": "Poha",
                "sunday_lunch": "Rice",
                "sunday_snacks": "Biscuits",
                "sunday_dinner": "Dal",
            }
        )

        response = self.client.post(url, data=form.data)
        menu = Menu.objects.get(hall=self.hall)
        self.assertRedirects(
            response, "/mess/menu", status_code=302, target_status_code=302
        )
        self.assertEqual(menu.month, "January")
        self.assertEqual(menu.monday_breakfast, "Poha")
        self.assertEqual(menu.monday_lunch, "Rice")
        self.assertEqual(menu.monday_snacks, "Biscuits")
        self.assertEqual(menu.monday_dinner, "Dal")

    def test_view_menu_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("view_menu")
        person = Client.objects.get(stakeholderID="22cs30060")
        perm3 = Permission.objects.get(name="is_menu")
        person.user_permissions.add(perm3)
        person.save()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "mess_manager/menu.html")
        self.assertEqual(response.context["items"][0][0], "Monday")
        self.assertEqual(response.context["items"][0][1], "A")
        self.assertEqual(response.context["month"], "January")

    def test_view_menu_student_get(self):
        self.client.login(username="22cs30061", password="Test@123")
        url = reverse("view_menu")
        person = Client.objects.get(stakeholderID="22cs30061")
        perm3 = Permission.objects.get(name="is_menu")
        person.user_permissions.add(perm3)
        person.save()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "mess_manager/menu.html")
        self.assertEqual(response.context["items"][0][0], "Monday")
        self.assertEqual(response.context["items"][0][1], "A")
        self.assertEqual(response.context["month"], "January")

    def test_generate_mess_passbook_manager(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("mess_passbook_pdf")
        self.assertEquals(url, "/mess/generate-passbook-pdf")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_generate_mess_passbook_warden(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("mess_passbook_pdf")
        self.assertEquals(url, "/mess/generate-passbook-pdf")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_add_ration_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("add_ration")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "mess_manager/add_ration.html")
        form = response.context["form"]
        self.assertIsInstance(form, RationForm)

    def test_add_ration_post(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("add_ration")
        form = RationForm(
            data={
                "item1": "Rice",
                "qt1": int(10),
                "rate1": int(10),
                "item2": "Dal",
                "qt2": int(19),
                "rate2": int(24),
                "item3": "Poha",
                "qt3": int(18),
                "rate3": int(15),
                "item4": "Biscuits",
                "qt4": int(15),
                "rate4": int(13),
                "item5": "Milk",
                "qt5": int(50),
                "rate5": int(20),
            }
        )
        response = self.client.post(url, data=form.data)
        ration = Ration.objects.get(hall=self.hall)
        self.assertRedirects(
            response, "/mess/passbook", status_code=302, target_status_code=200
        )
        self.assertEqual(ration.total, 2021)
