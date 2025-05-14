from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
import stripe

from .forms import ParentEmailForm
from packages.models import Package
from user_profiles.models import UserProfile
from checkout.models import Purchase
from django.utils import timezone
from datetime import timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


def checkout(request):
    """ A view to return the checkout page """
    
    return render(request, 'checkout/checkout.html')


@login_required
def who_is_paying(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    form = ParentEmailForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        request.session['parent_email'] = form.cleaned_data['parent_email']
        return redirect('start_checkout', package_id=package.id)

    return render(request, 'checkout/who_is_paying.html', {
        'form': form,
        'package': package
    })

@login_required
def start_checkout(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    parent_email = request.session.get('parent_email', None)

    if not parent_email:
        return redirect('who_is_paying', package_id=package.id)
    
    # Store package info for success view
    request.session['purchased_package_id'] = package.id
    request.session.modified = True

    # Create Stripe Checkout session
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
    )

    # Store Stripe metadata for confirmation
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

    # Save parent email to profile if provided
    if parent_email:
        profile.parent_email = parent_email
        profile.save()

        # Get student name from profile
        student_name = f"{profile.first_name} {profile.last_name}".strip() or request.user.username

        # Send confirmation email
        subject='Tutoring Package Confirmation',
        message=(
            f"Thank you for purchasing the {purchased_package.name} package.\n"
            f"Your card has been charged ${purchased_package.price:.2f}.\n"
            f"{student_name} now has {purchased_package.num_sessions} sessions available.\n"
            f"These sessions are valid until {expiration_date.strftime('%B %d, %Y')}.\n\n"
            "Students can log in to their profile to track or book sessions."
        )

        # Send to parent    
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[parent_email],
            fail_silently=False,
        )

        # Send to student if email is different than parent
        if request.user.email and request.user.email != parent_email:    
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[parent_email],
                fail_silently=False,
            )

    return render(request, 'checkout/checkout_success.html', {
        'package': purchased_package,
    })


@login_required
def checkout_cancel(request):
    return render(request, 'checkout/checkout_cancel.html')