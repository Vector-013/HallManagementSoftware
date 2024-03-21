from django.contrib import admin
from django.urls import path, include
from main import views as user_view
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", user_view.Login, name="login"),
    path(
        "logout/",
        user_view.Logout,
        name="logout",
    ),
    path("register/", user_view.register, name="register"),
    path("index/", user_view.index, name="index"),
    path("verify/<token>", user_view.verify, name="verify"),
    path("error", user_view.error_page, name="error"),
    path("view-complaints/", user_view.view_complaints, name="view_complaints"),
    path("make-complaints/", user_view.make_complaints, name="make_complaints"),
    path("", user_view.notice_student, name="notice"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
