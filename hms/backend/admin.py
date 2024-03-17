from django.contrib import admin
from .models import (
    AppUser,
    Student,
    HallClerk,
)

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin

# from .forms import (
#     PersonCreationForm,
#     PersonChangeForm,
#     StudentCreationForm,
#     StudentChangeForm,
#     WardenCreationForm,
# )


class AppUserAdmin(UserAdmin):
    # add_form = PersonCreationForm
    # form = PersonChangeForm
    model = AppUser
    list_display = ("username", "email", "first_name", "last_name", "role")
    list_filter = ("username", "role")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "address",
                    "mobile",
                    "role",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "address",
                    "mobile",
                    "first_name",
                    "last_name",
                    "role",
                    "is_superuser",
                    "groups",
                    "is_active",
                    "date_joined",
                ),
            },
        ),
    )
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


class StudentAdmin(ModelAdmin):
    model = Student
    # add_form = StudentCreationForm
    # form = StudentChangeForm

    def username(self, obj):
        return obj.appuser.username

    def first_name(self, obj):
        return obj.appuser.first_name

    def last_name(self, obj):
        return obj.appuser.last_name

    # def get_form(self, request, obj=None, **kwargs):
    #     defaults = {}
    #     if obj is None:
    #         defaults["form"] = self.add_form
    #     defaults.update(kwargs)
    #     return super().get_form(request, obj, **defaults)

    list_display = ("rollNumber", "username", "first_name", "last_name")


class HallClerkAdmin(ModelAdmin):
    model = HallClerk

    def name(self, obj):
        return obj.appuser.first_name + " " + obj.appuser.last_name


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(HallClerk, HallClerkAdmin)
