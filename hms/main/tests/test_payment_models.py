from django.test import TestCase
from ..models import *


class PaymentModelTesting(TestCase):

    def test_create_payment(self):
        hall = Hall.objects.create(
            name="Hall1",
            max_occupancy=100,
            blocks=1,
            floors=2,
            singles=10,
            doubles=10,
            triples=10,
        )
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

        sudent_passbook = StudentPassbook.objects.create(
            student=student,
        )

        self.assertEqual(
            sudent_passbook.__str__(), "Student Passbook: Ojas Dubey - 22cs30060"
        )
        due = Due.objects.create(
            demand=100,
            student_passbook=sudent_passbook,
            type="Mess Dues",
        )
        self.assertEqual(due.__str__(), "Mess Dues:Ojas Dubey - 22cs30060")

        warden_passbook = WardenPassbook.objects.create(
            hall=hall,
        )
        self.assertEqual(warden_passbook.__str__(), "Warden Passbook Hall1")
        hall_passbook = HallPassbook.objects.create(
            hall=hall,
        )
        self.assertEqual(hall_passbook.__str__(), "Hall Passbook Hall1")
        mess_passbook = MessPassbook.objects.create(
            hall=hall,
        )
        self.assertEqual(mess_passbook.__str__(), "Mess Passbook Hall1")
