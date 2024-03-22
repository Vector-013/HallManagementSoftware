from django import forms
from .models import *
from phonenumber_field.formfields import PhoneNumberField


class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            "stakeholderID",
            "email",
            "password",
            "mobile",
            "address",
            "role",
            "first_name",
            "last_name",
        )


class StudentRegistrationForm(forms.ModelForm):
    stakeholderID = forms.CharField(max_length=50)
    email = forms.EmailField(empty_value=None)
    password = forms.CharField(empty_value=None, max_length=400)
    mobile = PhoneNumberField()
    address = forms.CharField(widget=forms.Textarea)
    first_name = forms.CharField(max_length=150, empty_value=None)
    last_name = forms.CharField(max_length=150, empty_value=None)

    class Meta:
        model = Student
        fields = (
            "stakeholderID",
            "email",
            "password",
            "mobile",
            "address",
            "first_name",
            "last_name",
            "hall",
        )


# class NoticeRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Notice
#         fields = (
#             "title",
#             "content",
#             "role",
#         )


class ComplaintRegistrationForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = (
            "title",
            "content",
            "role",
        )
