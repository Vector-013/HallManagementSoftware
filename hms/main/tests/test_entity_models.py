from django.test import TestCase
from ..models import *


def build_rooms(hall):
    for i in range(hall.blocks):
        for j in range(hall.floors):
            for k in range(hall.singles):
                room = Room.objects.create(
                    hall=hall,
                    code=f"{chr(65+i)}{j+1}{k+1}",
                    sharing=1,
                    current_occupancy=0,
                )
                room.save()
            for k in range(hall.doubles):
                room = Room.objects.create(
                    hall=hall,
                    code=f"{chr(65+i)}{j+1}{k+1}",
                    sharing=2,
                    current_occupancy=0,
                )
                room.save()
            for k in range(hall.triples):
                room = Room.objects.create(
                    hall=hall,
                    code=f"{chr(65+i)}{j+1}{k+1}",
                    sharing=3,
                    current_occupancy=0,
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
        hall1.max_occupancy = hall1.calculate_max_occupancy()
        hall2.max_occupancy = hall2.calculate_max_occupancy()
        hall3.max_occupancy = hall3.calculate_max_occupancy()
        hall4.max_occupancy = hall4.calculate_max_occupancy()
        hall1.save()
        hall2.save()
        hall3.save()
        hall4.save()
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
        room1 = Room.objects.create(
            hall=hall1,
            code="A101",
            sharing=1,
            current_occupancy=0,
        )
        room1.current_occupancy += 1
        if room1.current_occupancy == room1.sharing:
            room1.is_free = False
        student1 = Student.objects.create(
            client=client1,
            hall=hall1,
            room=room1,
        )

        room2 = Room.objects.create(
            hall=hall1,
            code="A102",
            sharing=2,
            current_occupancy=0,
        )
        room2.current_occupancy += 1
        if room2.current_occupancy == room2.sharing:
            room2.is_free = False
        student2 = Student.objects.create(client=client2, hall=hall1, room=room2)

        room2.current_occupancy += 1
        if room2.current_occupancy == room2.sharing:
            room2.is_free = False
        student3 = Student.objects.create(client=client3, hall=hall1, room=room2)

        self.assertEqual(hall1.calculate_curr_occupancy(), 3)
