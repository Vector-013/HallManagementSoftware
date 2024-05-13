from django.test import TestCase
from ..models import *


class InteractionModelsTesting(TestCase):

    def test_create_interaction(self):
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
        notice = Notice.objects.create(
            title="Notice1",
            content="Lorem Ipsum Dolor Sit Amet Consectetur Adipiscing Elit",
            hall=hall,
        )
        self.assertEqual(notice.__str__(), "Notice1")

        complaint = Complaint.objects.create(
            title="Complaint1",
            content="Lorem Ipsum Dolor Sit Amet Consectetur Adipiscing Elit",
            hall=hall,
            student=student,
            status=False,
            category="maintenance",
        )
        self.assertEqual(complaint.__str__(), "Complaint1")
