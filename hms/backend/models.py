from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")

#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True")

#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True")

#         return self.create_user(email, password, **extra_fields)


class AppUserManager(BaseUserManager):
    def create_user(
        self, username, email, password, mobile, first_name, last_name, address, role
    ):
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            mobile=mobile,
            first_name=first_name,
            last_name=last_name,
            address=address,
            role=role,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, default="", unique=True)
    password = models.CharField(max_length=50, default="", unique=True)
    mobile = PhoneNumberField("Mobile Number", blank=False)
    first_name = models.CharField("first name", default="", max_length=150, blank=False)
    last_name = models.CharField("last name", default="", max_length=150, blank=False)
    address = models.TextField("Address", blank=False, default="")
    USERNAME_FIELD = "username"
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
        ("hall_clerk", "Hall Clerk"),
        ("hmc_chairman", "HMC Chairman"),
        ("mess_manager", "Mess Manager"),
        ("admin", "Administrator"),
        ("admission", "Admission Unit"),
    ]

    role = models.CharField(
        "Role", max_length=40, choices=ROLES, default="student", blank=False
    )

    class Meta:
        verbose_name = "AppUser"
        verbose_name_plural = "AppUsers"

    objects = AppUserManager()

    def __str__(self):
        return self.username


class Student(models.Model):
    appuser = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        related_name="student",
        primary_key=True,
        blank=False,
        unique=True,
    )

    rollNumber = models.CharField(
        "Roll Number", max_length=100, blank=False, unique=True
    )

    def _str_(self):
        return (
            self.appuser.first_name
            + " "
            + self.appuser.last_name
            + " - "
            + self.rollNumber
        )


class HallClerk(models.Model):
    appuser = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        related_name="hall_clerk",
        primary_key=True,
        blank=False,
        unique=True,
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(HallClerk, self).save(*args, **kwargs)
            self.appuser.role = "hall_clerk"
        else:
            self.appuser.role = "hall_clerk"
            super(HallClerk, self).save(*args, **kwargs)

    def _str_(self):
        return self.appuser.first_name + " " + self.appuser.last_name
