from django import forms
from .models import *


class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            "username",
            "email",
            "password",
            "mobile",
            "address",
            "role",
            "first_name",
            "last_name",
        )


class ComplaintRegistrationForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = (
            "title",
            "content",
            "role",
        )
