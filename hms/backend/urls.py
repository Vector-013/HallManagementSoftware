from django.urls import path
from . import views

urlpatterns = [
    path("student-register", views.StudentRegister.as_view(), name="student-register"),
    path(
        "hall-clerk-register",
        views.HallClerkRegister.as_view(),
        name="hall-clerk-register",
    ),
    path("login", views.UserLogin.as_view(), name="login"),
    path("logout", views.UserLogout.as_view(), name="logout"),
    path("user", views.UserView.as_view(), name="user"),
]
