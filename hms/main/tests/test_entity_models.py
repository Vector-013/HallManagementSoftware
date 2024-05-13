from django.test import TestCase
from ..models import *


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


class EntityModelTesting(TestCase):
    def test_hall(self):
        hall1 = Hall.objects.create(
            name="Hall1",
            blocks=3,
            floors=5,
            singles=30,
            doubles=25,
            triples=31,
        )  # 2595
        hall2 = Hall.objects.create(
            name="Hall2",
            blocks=7,
            floors=8,
            singles=13,
            doubles=22,
            triples=13,
        )  # 5376
        hall3 = Hall.objects.create(
            name="Hall3",
            blocks=2,
            floors=4,
            singles=12,
            doubles=20,
            triples=4,
        )  # 512
        hall4 = Hall.objects.create(
            name="Hall4",
            blocks=5,
            floors=4,
            singles=20,
            doubles=50,
            triples=11,
        )  # 3060
        hall1.save()
        hall2.save()
        hall3.save()
        hall4.save()
        build_rooms(hall1)
        build_rooms(hall2)
        build_rooms(hall3)
        build_rooms(hall4)
        hall1.max_occupancy = hall1.calculate_max_occupancy()
        hall2.max_occupancy = hall2.calculate_max_occupancy()
        hall3.max_occupancy = hall3.calculate_max_occupancy()
        hall4.max_occupancy = hall4.calculate_max_occupancy()

        self.assertEqual(hall1.max_occupancy, 2595)
        self.assertEqual(hall2.max_occupancy, 5376)
        self.assertEqual(hall3.max_occupancy, 512)
        self.assertEqual(hall4.max_occupancy, 3060)

        self.assertEqual(hall1.__str__(), "Hall1")
        self.assertEqual(hall2.__str__(), "Hall2")
        self.assertEqual(hall3.__str__(), "Hall3")
        self.assertEqual(hall4.__str__(), "Hall4")

        client1 = Client.objects.create_user(
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
        client2 = Client.objects.create_user(
            stakeholderID="22cs30061",
            email="shreya.bose.in@gmail.com",
            password="Test@123",
            mobile="+91 9234567890",
            first_name="Shreya",
            last_name="Bose",
            address="Bhopal",
            token="",
            role="student",
        )
        client3 = Client.objects.create_user(
            stakeholderID="22cs30062",
            email="qq639374@gmail.com",
            password="Test@123",
            mobile="+91 9234567890",
            first_name="Sakshi",
            last_name="Kumar",
            address="Bhopal",
            token="",
            role="student",
        )
        room1 = Room.objects.filter(hall=hall1).filter(is_free=True).first()
        room1.current_occupancy += 1
        if room1.current_occupancy == room1.sharing:
            room1.is_free = False
        room1.save()
        student1 = Student.objects.create(
            client=client1,
            hall=hall1,
            room=room1,
        )

        room2 = Room.objects.filter(hall=hall1).filter(is_free=True).first()
        room2.current_occupancy += 1
        if room2.current_occupancy == room2.sharing:
            room2.is_free = False
        room2.save()
        student2 = Student.objects.create(client=client2, hall=hall1, room=room2)

        room3 = Room.objects.filter(hall=hall1).filter(is_free=True).first()
        room3.current_occupancy += 1
        if room3.current_occupancy == room2.sharing:
            room3.is_free = False
        room3.save()
        student3 = Student.objects.create(client=client3, hall=hall1, room=room3)

        self.assertEqual(hall1.calculate_curr_occupancy(), 3)
        self.assertEqual(room1.__str__(), "Hall1-A00")
        self.assertEqual(room2.__str__(), "Hall1-A01")
        self.assertEqual(room3.__str__(), "Hall1-A010")
