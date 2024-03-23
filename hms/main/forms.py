from django import forms
from .models import *
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


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


class StudentSearchForm(forms.Form):
    stakeholderID = forms.CharField(label="Student ID", max_length=50)


class HallManagerRegistrationForm(forms.ModelForm):
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


class WorkerRegistrationForm(forms.ModelForm):
    stakeholderID = forms.CharField(max_length=50)
    email = forms.EmailField(empty_value=None)
    mobile = PhoneNumberField()
    address = forms.CharField(widget=forms.Textarea)
    first_name = forms.CharField(max_length=150, empty_value=None)
    last_name = forms.CharField(max_length=150, empty_value=None)

    class Meta:
        model = HallEmployee
        fields = (
            "stakeholderID",
            "email",
            "mobile",
            "address",
            "first_name",
            "last_name",
            "salary",
            "role",
        )


class ATRForm(forms.ModelForm):
    class Meta:
        model = ATR
        fields = (
            "complaint",
            "status",
            "employee",
            "report",
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
        fields = ("title", "content", "category", "image")


class PaymentForm(forms.Form):
    amount = forms.DecimalField(
        label="Amount",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )

    def __init__(self, total_due, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amount"].validators.append(MaxValueValidator(total_due))
        self.fields["amount"].initial = total_due
