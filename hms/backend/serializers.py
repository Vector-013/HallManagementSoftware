from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from .models import *

UserModel = get_user_model()


class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, clean_data):
        appuser = UserModel.objects.create_user(
            email=clean_data["email"],
            username=clean_data["username"],
            password=clean_data["password"],
            mobile=clean_data["mobile"],
            first_name=clean_data["first_name"],
            last_name=clean_data["last_name"],
            address=clean_data["address"],
            role="student",
        )
        student = Student.objects.create(
            appuser=appuser,
            rollNumber=clean_data["rollNumber"],
        )
        return student


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        print(clean_data["username"])
        user = authenticate(
            username=clean_data["username"], password=clean_data["password"]
        )
        print(clean_data["password"])
        print(user)
        if not user:
            raise ValidationError("user not found")
        return user


class HallClerkRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, clean_data):
        appuser = UserModel.objects.create_user(
            email=clean_data["email"],
            username=clean_data["username"],
            password=clean_data["password"],
            mobile=clean_data["mobile"],
            first_name=clean_data["first_name"],
            last_name=clean_data["last_name"],
            address=clean_data["address"],
            role="hall_clerk",
        )
        hall_clerk = HallClerk.objects.create(appuser=appuser)
        return hall_clerk


class StudentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"
