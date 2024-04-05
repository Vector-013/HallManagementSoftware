from django.test import TestCase
from ..models import *


class UserModelTesting(TestCase):

    # lets test the ClientManager.create_user method from the ClientManager class in models.py
    def test_create_user(self):
        user = Client.objects.create_user(
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

        self.assertIsInstance(user, Client)
        # test __str__ method of Client model
        self.assertEqual(user.__str__(), user.stakeholderID)

    def test_user_without_email(self):
        with self.assertRaises(ValueError):
            Client.objects.create_user(
                stakeholderID="22cs30060",
                email="",
                password="Test@123",
                mobile="+91 9234567890",
                first_name="Ojas",
                last_name="Dubey",
                address="Bhopal",
                token="",
                role="student",
            )

    def test_user_without_password(self):
        with self.assertRaises(ValueError):
            Client.objects.create_user(
                stakeholderID="22cs30060",
                email="ojasdubey13@gmail.com",
                password="",
                mobile="+91 9234567890",
                first_name="Ojas",
                last_name="Dubey",
                address="Bhopal",
                token="",
                role="student",
            )

    def test_superuser_without_email(self):
        with self.assertRaises(ValueError):
            Client.objects.create_superuser(
                stakeholderID="22cs30060",
                email="",
                password="Test@123",
                mobile="+91 9234567890",
                first_name="Ojas",
                last_name="Dubey",
            )

    def test_superuser_without_password(self):
        with self.assertRaises(ValueError):
            Client.objects.create_superuser(
                stakeholderID="22cs30060",
                email="ojasdubey13@gmail.com",
                password="",
                mobile="+91 9234567890",
                first_name="Ojas",
                last_name="Dubey",
            )

    def test_create_superuser(self):
        user = Client.objects.create_superuser(
            stakeholderID="22cs30060",
            email="ojasdubey13@gmail.com",
            password="Test@123",
            mobile="+91 9234567890",
            first_name="Ojas",
            last_name="Dubey",
        )

        self.assertIsInstance(user, Client)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(user.role, "admin")
        self.assertEqual(user.address, "Django")
        self.assertEqual(user.token, "")

    def test_student_str(self):
        client = Client.objects.create_user(
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
        hall = Hall.objects.create(
            name="Hall1",
            max_occupancy=100,
            blocks=1,
            floors=2,
            singles=10,
            doubles=10,
            triples=10,
        )
        room = Room.objects.create(
            hall=hall,
            code="A101",
            sharing=1,
            current_occupancy=1,
        )
        student = Student.objects.create(
            client=client,
            hall=hall,
            room=room,
        )
        self.assertEqual(
            student.__str__(),
            student.client.first_name + " " + student.client.last_name,
        )

    def test_hall_manager(self):
        client = Client.objects.create_user(
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
        hall = Hall.objects.create(
            name="Hall1",
            max_occupancy=100,
            blocks=1,
            floors=2,
            singles=10,
            doubles=10,
            triples=10,
        )
        # need to test save method of HallManager
        hall_manager = HallManager.objects.create(
            client=client,
            hall=hall,
        )

        hall_manager.save()
        self.assertEqual(hall_manager.client.role, "hall_manager")
        self.assertEqual(
            hall_manager.__str__(),
            hall_manager.client.first_name + " " + hall_manager.client.last_name,
        )

    def test_warden(self):
        client = Client.objects.create_user(
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
        hall = Hall.objects.create(
            name="Hall1",
            max_occupancy=100,
            blocks=1,
            floors=2,
            singles=10,
            doubles=10,
            triples=10,
        )
        # need to test save method of HallManager
        warden = Warden.objects.create(
            client=client,
            hall=hall,
        )

        warden.save()
        self.assertEqual(warden.client.role, "warden")
        self.assertEqual(
            warden.__str__(),
            warden.client.first_name + " " + warden.client.last_name,
        )

    def test_mess_manager(self):
        client = Client.objects.create_user(
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
        hall = Hall.objects.create(
            name="Hall1",
            max_occupancy=100,
            blocks=1,
            floors=2,
            singles=10,
            doubles=10,
            triples=10,
        )
        # need to test save method of HallManager
        mess_manager = MessManager.objects.create(
            client=client,
            hall=hall,
        )

        mess_manager.save()
        self.assertEqual(mess_manager.client.role, "mess_manager")
        self.assertEqual(
            mess_manager.__str__(),
            mess_manager.client.first_name + " " + mess_manager.client.last_name,
        )

    def test_hall_employee(self):
        client = Client.objects.create_user(
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
        hall = Hall.objects.create(
            name="Hall1",
            max_occupancy=100,
            blocks=1,
            floors=2,
            singles=10,
            doubles=10,
            triples=10,
        )
        # need to test save method of HallManager
        hall_employee = HallEmployee.objects.create(
            client=client,
            hall=hall,
        )

        hall_employee.save()
        self.assertEqual(hall_employee.client.role, "hall_employee")
        self.assertEqual(
            hall_employee.__str__(),
            hall_employee.client.first_name + " " + hall_employee.client.last_name,
        )
