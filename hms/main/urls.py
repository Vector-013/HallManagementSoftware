from django.contrib import admin
from django.urls import path, include
from main import views as user_view
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
# onclick="location.href={% url 'student_notice' %}"
urlpatterns = [
    path("", user_view.default_page, name="index"),
    path("admin/", admin.site.urls),
    path("login/", user_view.Login, name="login"),
    path("sign-up-options/", user_view.sign_up, name="sign_up_options"),
    path(
        "logout/",
        user_view.Logout,
        name="logout",
    ),
    path("register/", user_view.register, name="register"),
    path("register/", user_view.hall_manager_register, name="hall_manager_register"),
    path("index/", user_view.index, name="index"),
    path("verify/<token>", user_view.verify, name="verify"),
    path("error", user_view.error_page, name="error"),
    path("view-complaints/", user_view.view_complaints, name="view_complaints"),
    path("make-complaints/", user_view.make_complaints, name="make_complaints"),
    path("student/notice", login_required(user_view.notice_student), name="student_notice"),
    path("student/pay/success", user_view.payment_successful, name="success"),
    path("student/pay/cancel", user_view.payment_cancelled, name="cancel"),
    path("pay/stripe_webhook/", user_view.stripe_webhook, name="stripe_webhook"),
    path("student/passbook", user_view.student_passbook, name="student_passbook"),
    path("student/pay", user_view.pay, name="pay"),
    path(
        "hall/complaints", user_view.hall_view_complaints, name="hall_view_complaints"
    ),
    path("hall/create-atr", user_view.create_atr, name="create_atr"),
    path("hall/add-employee", user_view.add_employee, name="add_employee"),
    path(
        "warden/register-hall-manager",
        user_view.register_hall_manager,
        name="register_hall_manager",
    ),
    path(
        "verify-hall-manager/<token>",
        user_view.verify_hall_manager,
        name="verify_hall_manager",
    ),
    path("hall/search-student", user_view.search_student, name="search_student"),
    path(
        "hall/update-student-profile/<stakeholderID>",
        user_view.update_student_profile,
        name="update_student_profile",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
