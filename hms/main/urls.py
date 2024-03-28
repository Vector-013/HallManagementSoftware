from django.contrib import admin
from django.urls import path, include
from main import views as user_view
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static

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
    path("student/profile/", user_view.view_profile, name="view_profile"),
    path("student/make-complaints/", user_view.make_complaints, name="make_complaints"),
    path("student/notice", user_view.notice_student, name="student_notice"),
    path("student/passbook", user_view.student_passbook, name="student_passbook"),
    path("student/pay/success", user_view.payment_successful, name="success"),
    path("student/pay/cancel", user_view.payment_cancelled, name="cancel"),
    path("pay/stripe_webhook/", user_view.stripe_webhook, name="stripe_webhook"),
    path("student/pay", user_view.pay, name="pay"),
    path("hall/complaints", user_view.hall_complaints, name="hall_complaints"),
    path("hall/landing", user_view.hall_landing, name="hall_landing"),
    path("hall/passbook", user_view.hall_passbook, name="hall_passbook"),
    path("hall/create-atr", user_view.create_atr, name="create_atr"),
    path("hall/add-employee", user_view.add_employee, name="add_employee"),
    path("hall/approve-leaves", user_view.approve_leaves, name="approve_leaves"),
    path("hall/register-student/", user_view.register_student, name="register_student"),
    path(
        "hall/verify-student/<token>", user_view.verify_student, name="verify_student"
    ),
    path("hall/create-notice", user_view.make_notice, name="make_notice"),
    path("hall/search-student", user_view.search_student, name="search_student"),
    path(
        "hall/update-student-profile/<stakeholderID>",
        user_view.update_student_profile,
        name="update_student_profile",
    ),
    path("mess/landing", user_view.mess_landing, name="mess_landing"),
    path("mess/make-menu", user_view.make_menu, name="make_menu"),
    path("mess/menu", user_view.view_menu, name="view_menu"),
    path("mess/ration", user_view.add_ration, name="add_ration"),
    path("mess/passbook", user_view.mess_passbook, name="mess_passbook"),
    path(
        "warden/hall-manager",
        user_view.hall_manager,
        name="hall_manager",
    ),
    path(
        "warden/mess-manager",
        user_view.mess_manager,
        name="mess_manager",
    ),
    path(
        "warden/register-hall-manager",
        user_view.register_hall_manager,
        name="register_hall_manager",
    ),
    path(
        "warden/register-mess-manager",
        user_view.register_mess_manager,
        name="register_mess_manager",
    ),
    path(
        "warden/verify-manager/<token>",
        user_view.verify_manager,
        name="verify_manager",
    ),
    path("warden/passbook", user_view.warden_passbook, name="warden_passbook"),
    path("warden/hall-passbook", user_view.hall_passbook, name="hall_passbook"),
    path("warden/mess-passbook", user_view.mess_passbook, name="mess_passbook"),
    path("warden/landing", user_view.warden_landing, name="warden_landing"),
    path(
        "warden/generate-mess-demand",
        user_view.generate_mess_demand,
        name="generate_mess_demand",
    ),
    path(
        "warden/generate-hall-demand",
        user_view.generate_hall_demand,
        name="generate_hall_demand",
    ),
    path(
        "warden/generate-hall-salary",
        user_view.generate_salary,
        name="genrate_hall_salary",
    ),
    path(
        "hall/generate-passbook-pdf",
        user_view.generate_hall_passbook_pdf,
        name="hall_passbook_pdf",
    ),
    path(
        "hmc/register-hall",
        user_view.register_hall,
        name="register_hall",
    ),
    path(
        "hmc/register-warden",
        user_view.register_warden,
        name="register_warden",
    ),
    path(
        "hmc/verify-warden/<token>",
        user_view.verify_warden,
        name="verify_warden",
    ),
    path(
        "hmc/grant-allotment",
        user_view.grant_allotment,
        name="grant_allotment",
    ),
    path("hmc/landing", user_view.hmc_landing, name="hmc_admin"),
    path(
        "mess/generate-passbook-pdf",
        user_view.generate_mess_passbook_pdf,
        name="mess_passbook_pdf",
    ),
    path(
        "warden/generate-passbook-pdf",
        user_view.generate_warden_passbook_pdf,
        name="warden_passbook_pdf",
    ),
    path(
        "warden/allot_budget",
        user_view.allot_budget,
        name="allot_budget",
    ),
    path(
        "student/generate-atr-pdf/<int:pk>", user_view.generate_atr_pdf, name="atr_pdf"
    ),
    path("hall/approve_leaves", user_view.approve_leaves, name="approve_leaves"),
    path(
        "hmc/delete-warden",
        user_view.delete_warden,
        name="delete_warden",
    ),
    path(
        "warden/delete-hall-manager",
        user_view.delete_manager,
        name="delete_hall_manager",
    ),
    path(
        "warden/delete-mess-manager",
        user_view.delete_manager,
        name="delete_manager",
    ),
    path("hall/delete-student/", user_view.delete_student, name="delete_student"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
