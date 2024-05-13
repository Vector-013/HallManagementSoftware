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


class WardenViewTesting(TestCase):

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
            token="",
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

    def test_warden_view_profile(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("warden_view_profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "warden/profile.html")

    def test_hall_manager(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("hall_manager")
        person = Client.objects.get(stakeholderID="22cs30065")
        perm3 = Permission.objects.get(name="is_hall")
        person.user_permissions.add(perm3)
        person.save()
        response = self.client.get(url)
        self.assertRedirects(
            response, "/hall/profile", status_code=302, target_status_code=301
        )

    def test_hall_manager_without_manager(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("hall_manager")
        self.person.is_active = False
        self.person.save()
        response = self.client.get(url)
        self.assertRedirects(response, "/warden/register-hall-manager")
        self.person.is_active = True
        self.person.save()

    def test_mess_manager(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("mess_manager")
        person = Client.objects.get(stakeholderID="22cs30065")
        perm3 = Permission.objects.get(name="is_hall")
        person.user_permissions.add(perm3)
        person.save()
        response = self.client.get(url)
        self.assertRedirects(
            response,
            "/mess/profile",
            status_code=302,
            target_status_code=301,
        )

    def test_mess_manager_without_manager(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("mess_manager")
        self.messperson.is_active = False
        self.messperson.save()
        response = self.client.get(url)
        self.assertRedirects(response, "/warden/register-mess-manager")
        self.messperson.is_active = False
        self.messperson.save()

    def test_update_hall_manager_profile(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("update_hallmanager_profile")
        hall_manager = HallManager.objects.get(hall=self.hall)
        person = Client.objects.get(stakeholderID="22cs30065")
        perm3 = Permission.objects.get(name="is_hall")
        person.user_permissions.add(perm3)
        person.save()
        self.person.is_active = True
        self.person.save()

        form = UpdateHallManagerForm(
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
        self.assertEqual(hall_manager.client.first_name, "Test_one")
        self.assertEqual(hall_manager.client.last_name, "1")
        self.assertEqual(hall_manager.client.email, "test1@gmail.com")
        self.assertEqual(hall_manager.client.mobile, "+91 9234567891")
        self.assertEqual(hall_manager.client.address, "Delhi")
        self.assertRedirects(
            response, "/hall/profile", status_code=302, target_status_code=301
        )

    def test_update_hall_manager_without_manager(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("update_hallmanager_profile")
        self.person.is_active = False
        self.person.save()
        response = self.client.get(url)
        self.assertRedirects(response, "/warden/register-hall-manager")

    def test_update_hall_manager_profile_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("update_hallmanager_profile")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/update_manager_profile.html")
        form = response.context["form"]
        self.assertIsInstance(form, UpdateHallManagerForm)

    def test_update_mess_manager_profile(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("update_messmanager_profile")
        mess_manager = MessManager.objects.get(hall=self.hall)
        perm3 = Permission.objects.get(name="is_mess")
        self.warden.client.user_permissions.add(perm3)
        self.warden.client.save()

        form = UpdateMessManagerForm(
            data={
                "email": "test7@gmail.com",
                "mobile": "+91 9234567899",
                "first_name": "Test_onei",
                "last_name": "7",
                "address": "Delhi",
            }
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)

        self.assertEqual(mess_manager.client.first_name, "Test_onei")
        self.assertEqual(mess_manager.client.last_name, "7")
        self.assertEqual(mess_manager.client.email, "test7@gmail.com")
        self.assertEqual(mess_manager.client.mobile, "+91 9234567899")
        self.assertEqual(mess_manager.client.address, "Delhi")
        self.assertRedirects(
            response, "/mess/profile", status_code=302, target_status_code=301
        )

    def test_update_mess_manager_without_manager(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("update_messmanager_profile")
        self.mess_manager.client.is_active = False
        self.mess_manager.client.save()
        response = self.client.get(url)
        self.assertRedirects(response, "/warden/register-mess-manager")

    def test_update_mess_manager_profile_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("update_messmanager_profile")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/update_manager_profile.html")
        form = response.context["form"]
        self.assertIsInstance(form, UpdateMessManagerForm)

    def test_register_hall_manager_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("register_hall_manager")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/register_manager.html")
        form = response.context["form"]
        self.assertIsInstance(form, ManagerRegistrationForm)

    def test_register_hall_manager_post(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("register_hall_manager")
        form = ManagerRegistrationForm(
            data={
                "stakeholderID": "22cs30069",
                "email": "qq639374@gmail.com",
                "mobile": "+91 9234567891",
                "first_name": "Test_one",
                "last_name": "1",
                "address": "Delhi",
                "password": "Test@123",
            }
        )

        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/warden/landing")

    def test_register_mess_manager_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("register_mess_manager")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/register_manager.html")
        form = response.context["form"]
        self.assertIsInstance(form, ManagerRegistrationForm)

    def test_register_mess_manager_post(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("register_mess_manager")
        form = ManagerRegistrationForm(
            data={
                "stakeholderID": "22cs30069",
                "email": "qq639374@gmail.com",
                "mobile": "+91 9234567891",
                "first_name": "Test_one",
                "last_name": "1",
                "address": "Delhi",
                "password": "Test@123",
            }
        )

        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertRedirects(response, "/warden/landing")

    def test_verify_manager(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("verify_manager", args=[self.person.token])
        response = self.client.get(url)
        self.assertRedirects(response, "/warden/landing")

    def test_verify_manager_fail(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("verify_manager", args=["testtoken23"])
        response = self.client.get(url)
        self.assertRedirects(response, "/error")

    def test_delete_hall_manager(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("delete_hall_manager")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30060", "verify_password": "Test@123"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(HallManager.objects.count(), 0)
        self.assertTemplateUsed(response, "warden/delete_manager.html")

    def test_delete_hall_manager_exception(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("delete_hall_manager")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30060", "verify_password": "Test@1234"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(HallManager.objects.count(), 1)
        self.assertTemplateUsed(response, "warden/delete_manager.html")

    def test_delete_hall_manager_exception2(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("delete_hall_manager")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30055", "verify_password": "Test@123"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(HallManager.objects.count(), 1)
        self.assertTemplateUsed(response, "warden/delete_manager.html")

    def test_delete_hall_manager_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("delete_hall_manager")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/delete_manager.html")
        form = response.context["form"]
        self.assertIsInstance(form, DeleteUserForm)

    def test_delete_mess_manager(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("delete_mess_manager")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30068", "verify_password": "Test@123"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(MessManager.objects.count(), 0)
        self.assertTemplateUsed(response, "warden/delete_manager.html")

    def test_delete_mess_manager_exception(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("delete_mess_manager")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30068", "verify_password": "Test@1234"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(MessManager.objects.count(), 1)
        self.assertTemplateUsed(response, "warden/delete_manager.html")

    def test_delete_mess_manager_exception2(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("delete_mess_manager")

        form = DeleteUserForm(
            data={"stakeholderID": "22cs30055", "verify_password": "Test@123"}
        )
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=form.data)
        self.assertEqual(MessManager.objects.count(), 1)
        self.assertTemplateUsed(response, "warden/delete_manager.html")

    def test_delete_mess_manager_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("delete_mess_manager")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/delete_manager.html")
        form = response.context["form"]
        self.assertIsInstance(form, DeleteUserForm)

    def test_generate_warden_passbook(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("warden_passbook_pdf")
        self.assertEquals(url, "/warden/generate-passbook-pdf")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_warden_change_password(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("warden_change_password")
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
            response,
            "/warden/landing",
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30065", password="Test@1234"), True
        )

    def test_warden_change_password_fail(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("warden_change_password")
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
            response, "/warden/change-password", status_code=302, target_status_code=301
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30065", password="Test@123"), True
        )

    def test_warden_change_password_mismatch(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("warden_change_password")
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
            response, "/warden/change-password", status_code=302, target_status_code=301
        )
        self.client.logout()
        self.assertEqual(
            self.client.login(username="22cs30065", password="Test@123"), True
        )

    def test_hall_change_password_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("warden_change_password")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/change_password.html")
        form = response.context["form"]
        self.assertIsInstance(form, ChangePasswordForm)

    def test_generate_hall_demand(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("generate_hall_demand")
        form = VerifyForm(
            data={
                "verify_password": "Test@123",
                "amount": int(1000),
            }
        )

        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(
            response,
            "/warden/landing",
        )

    def test_generate_hall_demand_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("generate_hall_demand")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/verify_password.html")

    def test_generate_hall_demand_fail(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("generate_hall_demand")
        form = VerifyForm(
            data={
                "verify_password": "Test@1234",
                "amount": int(1000),
            }
        )

        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(
            response, "/login", status_code=302, target_status_code=301
        )

    def test_generate_mess_demand(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("generate_mess_demand")
        form = VerifyForm(
            data={
                "verify_password": "Test@123",
                "amount": int(1000),
            }
        )

        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(
            response,
            "/warden/landing",
        )

    def test_generate_mess_demand_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("generate_mess_demand")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/verify_password.html")

    def test_generate_mess_demand_fail(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("generate_mess_demand")
        form = VerifyForm(
            data={
                "verify_password": "Test@1234",
                "amount": int(1000),
            }
        )
        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(
            response, "/login", status_code=302, target_status_code=301
        )

    def test_generate_salary(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("generate_hall_salary")
        form = ConfirmForm(
            data={
                "verify_password": "Test@123",
            }
        )

        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(response, "/warden/landing")

    def test_generate_salary_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("generate_hall_salary")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/verify_password.html")

    def test_generate_salary_fail(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("generate_hall_salary")
        form = ConfirmForm(
            data={
                "verify_password": "Test@1234",
            }
        )
        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(
            response, "/login", status_code=302, target_status_code=301
        )

    def test_allot_budget(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("allot_budget")
        form = AllotmentForm(
            data={
                "verify_password": "Test@123",
                "hall_allotment": int(10000),
                "mess_allotment": int(20000),
            }
        )
        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(
            response,
            "/warden/passbook",
        )

    def test_allot_budget_fail(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("allot_budget")
        form = AllotmentForm(
            data={
                "verify_password": "Test@1234",
                "hall_allotment": int(10000),
                "mess_allotment": int(20000),
            }
        )
        response = self.client.post(url, data=form.data)
        self.assertTrue(form.is_valid())
        self.assertRedirects(
            response, "/login", status_code=302, target_status_code=301
        )

    def test_allot_budget_get(self):
        self.client.login(username="22cs30065", password="Test@123")
        url = reverse("allot_budget")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "warden/verify_password.html")
