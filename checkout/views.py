from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseBadRequest
import logging
import stripe

from datetime import timedelta
from .forms import ParentEmailForm
from packages.models import Package
from user_profiles.models import UserProfile
from checkout.models import Purchase

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)  # new


def checkout(request):
    """ A view to return the checkout page """   
    return render(request, 'checkout/checkout.html')


@login_required
def who_is_paying(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    # Clear stale data if arriving fresh
    if request.method == 'GET':
        request.session.pop('customer_email', None)
        request.session.pop('subject_id', None)

    form = ParentEmailForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        request.session['customer_email'] = form.cleaned_data['customer_email']
        selected_subject = form.cleaned_data['subject_choice']
        request.session['subject_id'] = selected_subject.id
        return redirect('start_checkout', package_id=package.id)
    
    return render(request, 'checkout/who_is_paying.html', {
        'form': form,
        'package': package
    })

@login_required
def start_checkout(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    customer_email = request.session.get('customer_email')
    subject_id = request.session.get('subject_id')

    logger.info("Checking session values:")
    logger.info(f" - Customer email: {customer_email}")
    logger.info(f" - Subject ID: {subject_id}")

    # Validate session state
    if not customer_email or not subject_id:
        messages.error(request, "Please enter buyer's email and select a subject before checkout.")
        request.session.pop('customer_email', None)
        request.session.pop('subject_id', None)
        return redirect('who_is_paying', package_id=package.id)
    
    # Store package info for success view
    request.session['purchased_package_id'] = package.id
    request.session.modified = True

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(package.price * 100),
                    'product_data': {'name': package.name},
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/checkout/success/'),
            cancel_url=request.build_absolute_uri('/checkout/cancel/'),
            customer_email=customer_email,
            payment_intent_data={
                'metadata': {
                'user_id': str(request.user.id),
                'package_id': str(package.id),
                'subject_id': str(subject_id),
                'customer_email': customer_email,
                }
            }
        )
    except Exception as e:
        logger.error(f" Stripe session creation failed: {e}")
        messages.error(request, "There was a problem connecting to Stripe. Please try again.")
        return redirect('who_is_paying', package_id=package.id)

    request.session['stripe_checkout_id'] = session.id
    request.session['stripe_payment_intent'] = session.payment_intent

    return redirect(session.url, code=303)


@login_required
def checkout_success(request):
    # Extract what you need before clearing
    purchase = Purchase.objects.filter(user=request.user).order_by('-purchased_on').first()
    package = purchase.package if purchase else None

    # Now clear all relevant session keys
    for key in [
        'customer_email',
        'subject_id',
        'purchased_package_id',
        'stripe_checkout_id',
        'stripe_payment_intent'
    ]:
        request.session.pop(key, None)

    return render(request, 'checkout/checkout_success.html', {
        'package': package,
        'purchase': purchase,

    })


@login_required
def checkout_cancel(request):
    keys_to_clear = [
        'customer_email',
        'subject_id',
        'purchased_package_id',
        'stripe_checkout_id',
        'stripe_payment_intent',
    ]
    for key in keys_to_clear:
        request.session.pop(key, None)

    return render(request, 'checkout/checkout_cancel.html')