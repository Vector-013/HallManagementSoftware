from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from ..models import *
from ..forms import PaymentForm
import stripe
import time


def student_passbook(request):
    print("-----------------------------------", request.user)
    student = Student.objects.filter(client=request.user).first()
    passbook = StudentPassbook.objects.filter(student=student).first()
    dues = passbook.dues.order_by("-timestamp")
    payments = passbook.student_payment.order_by("-timestamp")
    total_due = dues.aggregate(total=Sum("demand"))["total"]
    total_paid = payments.aggregate(total=Sum("fulfilled"))["total"]
    if not total_paid:
        total_outstanding = total_due
    else:
        try:
            total_outstanding = total_due - total_paid
        except:
            total_outstanding = 0

    context = {
        "dues": dues,
        "payments": payments,
        "total_due": total_due,
        "total_paid": total_paid,
        "total_outstanding": total_outstanding,
    }

    return render(request, "student/passbook.html", context)


def hall_passbook(request):

    hall_manager = HallManager.objects.filter(client=request.user)[0]
    hall = hall_manager.hall
    passbook = HallPassbook.objects.filter(hall=hall)[0]
    expenditures = passbook.hall_expenditure.order_by("-timestamp")
    total_expenditures = expenditures.aggregate(total=Sum("expenditure"))["total"]
    original_budget = passbook.budget
    try:
        current_budget = original_budget - total_expenditures
    except:
        current_budget = original_budget

    context = {
        "original_budget": original_budget,
        "expenditures": expenditures,
        "total_expenditures": total_expenditures,
        "current_budget": current_budget,
        "original_budget": original_budget,
    }

    return render(request, "hall_manager/passbook.html", context)


def mess_passbook(request):

    mess_manager = MessManager.objects.filter(client=request.user).first()
    hall = mess_manager.hall
    passbook = MessPassbook.objects.filter(hall=hall).first()
    expenditures = passbook.mess_expenditure.order_by("-timestamp")
    total_expenditures = expenditures.aggregate(total=Sum("expenditure"))["total"]
    original_budget = passbook.budget
    try:
        current_budget = original_budget - total_expenditures
    except:
        current_budget = original_budget

    context = {
        "original_budget": original_budget,
        "expenditures": expenditures,
        "total_expenditures": total_expenditures,
        "current_budget": current_budget,
        "original_budget": original_budget,
    }

    return render(request, "mess_manager/passbook.html", context)


# def warden_passbook(request):

#     if request.user.role != "warden":
#         return redirect("login/")

#     warden = Warden.objects.filter(client=request.user)[0]
#     hall = Warden.hall
#     passbook = WardenPassbook.objects.filter(hall=hall)[0]
#     payments = passbook.student_payment.order_by("-timestamp")
#     total_spent = expenditure.aggregate(total=Sum("demand"))["total"]
#     total_paid = payments.aggregate(total=Sum("fulfilled"))["total"]
#     try:
#         current_budget = total_due - total_paid
#     except:
#         total_outstanding = 0

#     context = {
#         "expenditure": expenditure,
#         "payments": payments,
#         "total_spent": total_spent,
#         "total_paid": total_paid,
#         "current_budget": current_budget,
#     }

#     return render(request, "student/passbook.html", context)


def pay(request):
    if request.user.role != "student":
        return redirect("/login")

    student = Student.objects.filter(client=request.user)[0]
    passbook = StudentPassbook.objects.filter(student=student)[0]
    dues = passbook.dues.all()
    payments = passbook.student_payment.all()
    total_due = dues.aggregate(total=Sum("demand"))["total"]
    total_paid = payments.aggregate(total=Sum("fulfilled"))["total"]

    if total_paid is not None and total_due is not None:
        total_due = total_due - total_paid

    total_due = total_due
    total_paid = total_paid
    if total_due is not None and total_due > 0:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer = stripe.Customer.create(
            name=student.client.first_name,
            address={
                "line1": "room hall",
                "postal_code": "721302",
                "city": "kgp",
                "state": "wb",
                "country": "US",
            },
        )
        if request.method == "POST":
            form = PaymentForm(total_due, request.POST)
            if form.is_valid():
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    customer=customer.id,
                    line_items=[
                        {
                            "price_data": {
                                "currency": "inr",
                                "unit_amount": int(
                                    form.cleaned_data["amount"] * 100
                                ),  # convert the price to cents
                                "product_data": {
                                    "name": "Fees",
                                },
                            },
                            "quantity": 1,
                        },
                    ],
                    mode="payment",
                    # customer_creation="always",
                    success_url=settings.REDIRECT_URL
                    + "/student/pay/success?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=settings.REDIRECT_URL + "/student/pay/cancel",
                )
                return redirect(checkout_session.url, code=303)
            else:
                return render(
                    request,
                    "student/payment_form.html",
                    {"form": form, "total_due": total_due},
                )
        else:
            form = PaymentForm(total_due=round(total_due, 2))

        return render(
            request,
            "student/payment_form.html",
            {"form": form, "total_due": round(total_due, 2)},
        )
    else:
        messages.add_message(request, messages.INFO, "You have no dues left")
        return redirect("student/passbook")


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get("session_id", None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    student = Student.objects.filter(client=request.user).first()
    passbook = StudentPassbook.objects.filter(student=student).first()
    if not Payments.objects.filter(
        student=student, stripe_checkout_id=checkout_session_id, payment_bool=True
    ):
        user_payment = Payments.objects.create(
            student=student, stripe_checkout_id=checkout_session_id, payment_bool=True
        )
        user_payment.save()
        StudentPayment.objects.create(
            student_passbook=passbook, fulfilled=Decimal(session.amount_total) / 100
        )
        messages.success(request, messages.SUCCESS, "Payment Successful")
    return render(request, "student/payment_success.html", context={"customer": customer})


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return render(request, "student/payment_cancelled.html")


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(10)
    payload = request.body
    signature_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = event["data"]["object"]
        time.sleep(15)
        payments = Payments.objects.get(stripe_checkout_id=session_id)
        # line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        payments.payment_bool = True
        payments.save()
    return HttpResponse(status=200)
