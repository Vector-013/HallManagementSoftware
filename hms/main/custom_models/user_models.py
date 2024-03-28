from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from .entity_models import Hall, Room


class ClientManager(BaseUserManager):
    def create_user(
        self,
        stakeholderID,
        email,
        password,
        mobile,
        first_name,
        last_name,
        address,
        token,
        role,
    ):
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            stakeholderID=stakeholderID,
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            address=address,
            token=token,
            role=role,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, stakeholderID, email, password, mobile, first_name, last_name
    ):
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        user = self.create_user(
            stakeholderID,
            email,
            password,
            mobile,
            first_name,
            last_name,
            "Django",
            "",
            "admin",
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class Client(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=False)
    stakeholderID = models.CharField(
        max_length=50, default="", unique=True, blank=False
    )
    password = models.CharField(max_length=400, default="", unique=False)
    mobile = PhoneNumberField("Mobile Number", blank=False)
    first_name = models.CharField("first name", default="", max_length=150, blank=False)
    last_name = models.CharField("last name", default="", max_length=150, blank=False)
    address = models.TextField("Address", blank=False, default="")
    USERNAME_FIELD = "stakeholderID"
    REQUIRED_FIELDS = [
        "password",
        "email",
        "mobile",
        "first_name",
        "last_name",
    ]

    ROLES = [
        ("student", "Student"),
        ("warden", "Warden"),
        ("hall_manager", "Hall Manager"),
        ("hmc_chairman", "HMC Chairman"),
        ("mess_manager", "Mess Manager"),
        ("admin", "Administrator"),
        ("admission", "Admission Unit"),
        ("hall_employee", "Hall Employee"),
    ]

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateField(default=datetime.now, blank=True)
    token = models.CharField(max_length=100, default="")

    role = models.CharField(
        "Role", max_length=40, choices=ROLES, default="student", blank=False
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    objects = ClientManager()

    def __str__(self):
        return self.stakeholderID


class Student(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="student",
        primary_key=True,
        blank=False,
        unique=True,
    )

    hall = models.ForeignKey(
        Hall,
        related_name="student_hall",
        on_delete=models.CASCADE,
    )

    room = models.ForeignKey(
        Room,
        related_name="student_room",
        on_delete=models.CASCADE,
    )

    def _str_(self):
        return self.client.first_name + " " + self.client.last_name


class HallManager(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="hall_manager",
        primary_key=True,
        blank=False,
        unique=True,
    )

    hall = models.ForeignKey(
        Hall, related_name="manager_hall", on_delete=models.CASCADE, default=None
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(HallManager, self).save(*args, **kwargs)
            self.client.role = "hall_manager"
        else:
            self.client.role = "hall_manager"
            super(HallManager, self).save(*args, **kwargs)

    def _str_(self):
        return self.client.first_name + " " + self.client.last_name


class Warden(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="warden",
        primary_key=True,
        blank=False,
        unique=True,
    )

    hall = models.ForeignKey(
        Hall, related_name="warden", on_delete=models.CASCADE, default=None
    )

    department = models.CharField("Department", max_length=50, default="")
    designation = models.CharField("Designation", max_length=200, default="")
    posts_held = models.CharField("Posts Held", max_length=500, default="")

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(Warden, self).save(*args, **kwargs)
            self.client.role = "warden"
        else:
            self.client.role = "warden"
            super(Warden, self).save(*args, **kwargs)

    def _str_(self):
        return self.client.first_name + " " + self.client.last_name


class MessManager(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="mess_manager",
        primary_key=True,
        blank=False,
        unique=True,
    )

    hall = models.ForeignKey(
        Hall, related_name="mess_hall", on_delete=models.CASCADE, default=None
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(MessManager, self).save(*args, **kwargs)
            self.client.role = "mess_manager"
        else:
            self.client.role = "mess_manager"
            super(MessManager, self).save(*args, **kwargs)

    def _str_(self):
        return self.client.first_name + " " + self.client.last_name


class HallEmployee(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="hall_employee",
        primary_key=True,
        blank=False,
        unique=True,
    )

    hall = models.ForeignKey(
        Hall,
        default=None,
        related_name="employee_hall",
        on_delete=models.CASCADE,
    )

    role = models.CharField(
        "Role",
        max_length=20,
        choices=[
            ("gardener", "Garderner"),
            ("plumber", "Plumber"),
            ("electrician", "Electrician"),
            ("hall_canteen", "Hall Canteen"),
            ("sweeper", "Sweeper"),
            ("cook", "Cook"),
            ("security", "Security"),
            ("mess_worker", "Mess Worker"),
        ],
        default="Mess Worker",
        blank=False,
    )

    salary = models.IntegerField(
        "Salary",
        choices=[
            (1000, "1000"),
            (2000, "2000"),
            (5000, "5000"),
            (10000, "10000"),
            (15000, "15000"),
            (20000, "20000"),
        ],
        default=2000,
        blank=False,
    )

    monthly_leaves = models.IntegerField("monthly leaves taken", default=0)

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(HallEmployee, self).save(*args, **kwargs)
            self.client.role = "hall_employee"
        else:
            self.client.role = "hall_employee"

            super(HallEmployee, self).save(*args, **kwargs)

    def _str_(self):
        return self.client.first_name + " " + self.client.last_name


class HMC(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="hmc",
        primary_key=True,
        blank=False,
        unique=True,
    )
