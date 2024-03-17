from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path(
        "student-register",
        permission_required("backend.add_student")(views.StudentRegister.as_view()),
        name="student-register",
    ),
    path(
        "hall-clerk-register",
        views.HallClerkRegister.as_view(),
        name="hall-clerk-register",
    ),
    path("login", views.UserLogin.as_view(), name="login"),
    path("logout", views.UserLogout.as_view(), name="logout"),
    path("user", views.UserView.as_view(), name="user"),
]
