from django.contrib import admin
from django.urls import path, include
from main import views as user_view
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
# onclick="location.href={% url 'student_notice' %}"
urlpatterns = [
    path("", user_view.entry, name="entry"),
    path("admin/", admin.site.urls),
    path("login/", user_view.Login, name="login"),
    path(
        "logout/",
        user_view.Logout,
        name="logout",
    ),
    path("error", user_view.error_page, name="error"),
    path("student/view-complaints/", user_view.view_complaints, name="view_complaints"),
    path("student/make-complaints/", user_view.make_complaints, name="make_complaints"),
    path("student/notice", user_view.notice_student, name="notice"),
    path("student/passbook", user_view.student_passbook, name="student_passbook"),
    path("student/pay/success", user_view.payment_successful, name="success"),
    path("student/pay/cancel", user_view.payment_cancelled, name="cancel"),
    path("pay/stripe_webhook/", user_view.stripe_webhook, name="stripe_webhook"),
    path("student/pay", user_view.pay, name="pay"),
    path("hall/complaints", user_view.hall_complaints, name="hall_complaints"),
    path("hall/landing", user_view.hall_landing, name="hall_landing"),
    path("hall/create-atr", user_view.create_atr, name="create_atr"),
    path("hall/add-employee", user_view.add_employee, name="add_employee"),
    path("hall/register-student/", user_view.register_student, name="register_student"),
    path(
        "hall/verify-student/<token>", user_view.verify_student, name="verify_student"
    ),
    path("hall/search-student", user_view.search_student, name="search_student"),
    path(
        "hall/update-student-profile/<stakeholderID>",
        user_view.update_student_profile,
        name="update_student_profile",
    ),
    path(
        "warden/register-hall-manager",
        user_view.register_hall_manager,
        name="register_hall_manager",
    ),
    path(
        "warden/verify-hall-manager/<token>",
        user_view.verify_hall_manager,
        name="verify_hall_manager",
    ),
    path("warden/landing", user_view.warden_landing, name="warden_landing"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
