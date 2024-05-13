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


class HMCViewTesting(TestCase):

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
            token="asdfghjkl",
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
            token="qqaazz",
            role="warden",
        )
        perm = Permission.objects.get(name="is_warden")
        # perm2 = Permission.objects.get(name="is_hall")
        self.wperson.user_permissions.add(perm)
        # self.wperson.user_permissions.add(perm2)
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

        self.messperson = Client.objects.create_user(
            stakeholderID="22cs30068",
            email="shreya.bose.in@gmail.com",
            password="Test@123",
            mobile="+91 9234567890",
            first_name="Shreya",
            last_name="Bose",
            address="Bhopal",
            token="",
            role="mess_manager",
        )
        perm = Permission.objects.get(name="is_mess")

        self.messperson.user_permissions.add(perm)

        self.messperson.is_active = True
        self.messperson.save()

        self.mess_manager = MessManager.objects.create(
            client=self.messperson, hall=self.hall
        )

        self.hmcperson = Client.objects.create_user(
            stakeholderID="22cs30069",
            email="shreya.bose.in@gmail.com",
            password="Test@123",
            mobile="+91 9234567890",
            first_name="Shreya",
            last_name="Bose",
            address="Bhopal",
            token="",
            role="hmc_chairman",
        )
        perm = Permission.objects.get(name="is_HMC")

        self.hmcperson.user_permissions.add(perm)

        self.hmcperson.is_active = True
        self.hmcperson.save()

        self.hmc = HMC.objects.create(client=self.hmcperson)

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
        self.mess_passbook = MessPassbook.objects.create(hall=self.hall)
        self.hall_passbook = HallPassbook.objects.create(hall=self.hall)
        self.transaction = HallTransaction.objects.create(
            type="Salaries",
            amount=1000,
            hall_passbook=self.hall_passbook,
            timestamp=datetime.now(pytz.timezone("Asia/Kolkata")),
        )
        self.warden_passbook = WardenPassbook.objects.create(hall=self.hall)
        self.wtransaction = WardenTransaction.objects.create(
            type="Grant",
            amount=1000,
            warden_passbook=self.warden_passbook,
            timestamp=datetime.now(pytz.timezone("Asia/Kolkata")),
        )
        self.student_passbook1 = StudentPassbook.objects.create(student=self.student1)
        self.student_passbook2 = StudentPassbook.objects.create(student=self.student2)
        self.student_passbook3 = StudentPassbook.objects.create(student=self.student3)
        self.student_passbook4 = StudentPassbook.objects.create(student=self.student4)

    def test_delete_warden(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("delete_warden")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30065", "verify_password": "Test@123"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(Warden.objects.count(), 0)
        self.assertTemplateUsed(response, "hmc/delete_warden.html")

    def test_delete_warden_exception(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("delete_warden")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30065", "verify_password": "Test@1234"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(Warden.objects.count(), 1)
        self.assertTemplateUsed(response, "hmc/delete_warden.html")

    def test_delete_warden_exception2(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("delete_warden")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30055", "verify_password": "Test@123"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(MessManager.objects.count(), 1)
        self.assertTemplateUsed(response, "hmc/delete_warden.html")

    def test_delete_warden_get(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("delete_warden")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hmc/delete_warden.html")
        form = response.context["form"]
        self.assertIsInstance(form, DeleteUserForm)

    def test_grant_allotment(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("grant_allotment")
        hall = self.hall
        form = GrantForm(
            data={"verify_password": "Test@123", "amount": int(20000), "hall": hall}
        )
        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(
            response,
            "/hmc/landing",
        )

    def test_grant_allotment_fail(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("grant_allotment")
        form = GrantForm(
            data={
                "verify_password": "Test@1234",
                "hall": self.hall,
                "amount": int(20000),
            }
        )
        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(
            response, "/login", status_code=302, target_status_code=301
        )

    def test_grant_allotment_get(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("grant_allotment")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hmc/grant_allotment.html")

    def test_view_halls(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("view_halls")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hmc/view_halls.html")

    def test_hmc_landing(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("hmc_landing")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hmc/landing.html")

    def test_register_hall(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("register_hall")
        form = HallRegistrationForm(
            data={
                "name": "Hall6",
                "blocks": int(2),
                "floors": int(3),
                "singles": int(10),
                "rent_singles": int(2000),
                "doubles": int(10),
                "rent_doubles": int(2000),
                "triples": int(10),
                "rent_triples": int(2000),
            }
        )
        hall_new = Hall.objects.filter(name="Hall6")
        response = self.client.post(url, data=form.data)
        hall_new = Hall.objects.filter(name="Hall6")
        self.assertRedirects(response, "/hmc/view-halls")

    def test_register_hall_get(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("register_hall")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hmc/hall_registration.html")

    def test_register_warden_get(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("register_warden")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hmc/register_warden.html")
        form = response.context["form"]
        self.assertIsInstance(form, WardenRegistrationForm)

    def test_register_warden_post(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("register_warden")
        form = WardenRegistrationForm(
            data={
                "stakeholderID": "22cs30071",
                "email": "qq639374@gmail.com",
                "mobile": "+91 9234567891",
                "first_name": "Test_one",
                "last_name": "1",
                "address": "Delhi",
                "password": "Test@123",
                "department": "CSE",
                "designation": "Warden",
                "posts_held": "None",
                "hall": self.hall.id,
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        new_warden = Client.objects.get(stakeholderID="22cs30071")
        self.assertRedirects(response, "/hmc/landing")
        self.assertEqual(new_warden.email, "qq639374@gmail.com")
        self.assertEqual(new_warden.mobile, "+91 9234567891")
        self.assertEqual(new_warden.first_name, "Test_one")
        self.assertEqual(new_warden.last_name, "1")
        self.assertEqual(new_warden.address, "Delhi")

    def test_search_warden_get(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("search_warden")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hmc/search_warden.html")
        form = response.context["form"]
        self.assertIsInstance(form, UserSearchForm)

    def test_search_warden_post(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("search_warden")
        form = UserSearchForm(data={"stakeholderID": "22cs30065"})
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/hmc/update-warden-profile/22cs30065")

    def test_search_warden_post_invalid(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("search_warden")
        form = UserSearchForm(data={"stakeholderID": "22cs30061"})
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/hmc/search-warden")

    def test_search_warden_post_invalid2(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("search_warden")
        form = UserSearchForm(data={"stakeholderID": "22cs30086"})
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/hmc/search-warden")

    def test_verify_warden(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("verify_warden", args=[self.wperson.token])
        response = self.client.get(url)
        self.assertRedirects(response, "/hmc/landing")

    def test_verify_warden_invalid(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("verify_warden", args=["invalid_token"])
        response = self.client.get(url)
        self.assertRedirects(response, "/error")

    def test_update_warden(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("update_warden_profile", args=["22cs30065"])
        form = UpdateWardenForm(
            data={
                "email": "test@gmail.com",
                "mobile": "+91 9234567890",
                "first_name": "Test",
                "last_name": "1",
                "address": "Bhopal",
                "department": "CSE",
                "designation": "Warden",
                "posts_held": "None",
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(
            response,
            "/hmc/search-warden",
        )

    def test_update_warden_get(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("update_warden_profile", args=["22cs30065"])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hmc/update_warden_profile.html")

    def test_hmc_change_password(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("hmc_change_password")
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
            response, "/hmc/landing"
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30069", password="Test@1234"), True
        )

    def test_hmc_change_password_fail(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("hmc_change_password")
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
            response, "/hmc/change-password", status_code=302, target_status_code=301
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30069", password="Test@123"), True
        )

    def test_hmc_change_password_mismatch(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("hmc_change_password")
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
            response, "/hmc/change-password", status_code=302, target_status_code=301
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30069", password="Test@123"), True
        )

    def test_hmc_change_password_get(self):
        self.client.login(username="22cs30069", password="Test@123")
        url = reverse("hmc_change_password")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "hmc/change_password.html")
        form = response.context["form"]
        self.assertIsInstance(form, ChangePasswordForm)

    def test_hmc_view_profile(self):
        self.client.login(username="22cs30069", password="Test@123")
        response = self.client.get(reverse("hmc_view_profile"))
        self.assertTemplateUsed(response, "hmc/profile.html")
        self.assertEqual(response.context["hmc"], self.hmc)
