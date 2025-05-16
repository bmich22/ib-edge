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
        request.session.pop('parent_email', None)
        request.session.pop('subject_name', None)
        request.session.pop('subject_id', None)

    form = ParentEmailForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        request.session['parent_email'] = form.cleaned_data['parent_email']
        subject = form.cleaned_data['subject']
        request.session['subject_id'] = subject.id  
        request.session['subject_name'] = subject.name
        return redirect('start_checkout', package_id=package.id)
    
    return render(request, 'checkout/who_is_paying.html', {
        'form': form,
        'package': package
    })

@login_required
def start_checkout(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    parent_email = request.session.get('parent_email')
    subject_name = request.session.get('subject_name')

    logger.info("Checking session values:")
    logger.info(f" - Parent email: {parent_email}")
    logger.info(f" - Subject name: {subject_name}")

    # Validate session state
    if not parent_email or not subject_name or subject_name == 'Unknown':
        messages.error(request, "Please enter parent email and select a subject before checkout.")
        request.session.pop('parent_email', None)
        request.session.pop('subject_name', None)
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
            customer_email=parent_email,
            payment_intent_data={
                'metadata': {
                    'user_id': str(request.user.id),
                    'package_id': str(package.id),
                    'subject': subject_name,
                    'customer_email': parent_email,
                    'package_price': package.price,
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
    user = request.user
    profile = user.userprofile
    parent_email = request.session.pop('parent_email', None)
    package_id = request.session.pop('purchased_package_id', None)
    stripe_checkout_id = request.session.pop('stripe_checkout_id', None)
    stripe_payment_intent = request.session.pop('stripe_payment_intent', None)

    if not package_id:
        return render(request, 'checkout/checkout_success.html')  # fallback

    purchased_package = get_object_or_404(Package, id=package_id)
    expiration_date = timezone.now() + timedelta(weeks=8)

    # Create a purchase record
    Purchase.objects.create(
        user=user,
        package=purchased_package,
        expires_on=expiration_date,
        stripe_checkout_id=stripe_checkout_id,
        stripe_payment_intent=stripe_payment_intent,
        payment_status='paid',
    )

    profile.total_sessions_available += purchased_package.num_sessions
    profile.save()

    return render(request, 'checkout/checkout_success.html', {
        'package': purchased_package,
    })


@login_required
def checkout_cancel(request):
    return render(request, 'checkout/checkout_cancel.html')