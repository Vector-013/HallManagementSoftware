from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from custom_models.payment_models import Payments, StudentPayment
from ..forms import PaymentForm
import stripe
import time



@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = Payments.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)

def passbook(request):
    if request.user.role != "student":
        return redirect("index")

    student = request.user.student
    passbook = student.passbook
    dues = passbook.dues.order_by('-timestamp')
    payments = passbook.payments.order_by('-timestamp')
    total_due = dues.aggregate(total=Sum('demand'))['total']
    total_paid = payments.aggregate(total=Sum('fulfilled'))['total']

    context = {
        'dues': dues,
        'payments': payments,
        'total_due': total_due,
        'total_paid': total_paid,
    }

    return render(request, 'studentIndex/passbook.html', context)


def pay(request):
    if request.user.role != "student":
        return redirect("index")
    dues = request.user.student.passbook.dues.all()
    payments = request.user.student.passbook.payments.all()
    total_due = dues.aggregate(total = Sum('demand'))['total']
    total_paid = payments.aggregate(total = Sum('fulfilled'))['total']
    
    if total_paid is not None and total_due is not None:
        total_due = total_due - total_paid
    
    total_due = total_due
    total_paid = total_paid
    if total_due is not None and total_due > 0:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if request.method == 'POST':
            form = PaymentForm(total_due, request.POST)
            if form.is_valid():
                checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(form.cleaned_data['amount']*100), # convert the price to cents
                        'product_data': {
                            'name': 'Fees',
                        },
                    },
                    'quantity': 1,
                },
                ],
                mode='payment',
                customer_creation = 'always',
                success_url=settings.REDIRECT_URL + '/passbook/pay/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.REDIRECT_URL + '/passbook/pay/cancel',
                )
                return redirect(checkout_session.url, code=303)
            else:
                return render(request, 'studentIndex/payment-form.html', {'form': form, 'total_due': total_due})
        else:
            form = PaymentForm(total_due=round(total_due, 2))

        return render(request, 'studentIndex/payment-form.html', {'form': form, 'total_due': round(total_due, 2)})
    else:
        messages.add_message(request, messages.INFO, "You have no dues left")
        return redirect("passbook")


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    student = request.user.student
    if not Payments.objects.filter(student=student, stripe_checkout_id = checkout_session_id, payment_bool=True):
        user_payment = Payments.objects.create(student=student, stripe_checkout_id = checkout_session_id, payment_bool=True)
        user_payment.save()
        StudentPayment.objects.create(passbook = student.passbook, fulfilled = Decimal(session.amount_total)/100)
        
    return render(request, 'studentIndex/payment-successful.html', {'customer': customer})

def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	return render(request, 'studentIndex/payment-cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
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
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = event['data']['object']
        time.sleep(15)
        payments = Payments.objects.get(stripe_checkout_id=session_id)
        # line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        payments.payment_bool = True
        payments.save()
    return HttpResponse(status=200)