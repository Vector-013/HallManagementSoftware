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
        self.person.user_permissions.add(perm)
        self.person.user_permissions.add(perm2)
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

    def test_mess_view_manager_get(self):
        self.client.login(username="22cs30060", password="Test@123")
        url = reverse("mess_view_profile")
        response = self.client.get(url)
