from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
import stripe

from .forms import ParentEmailForm
from packages.models import Package
from user_profiles.models import UserProfile
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


def checkout(request):
    """ A view to return the reviews page """
    
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
    
    request.session['purchased_package_id'] = package.id
    request.session.modified = True

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

    return redirect(session.url, code=303)


@login_required
def checkout_success(request):
    profile = request.user.userprofile
    parent_email = request.session.pop('parent_email', None)
    package_id = request.session.pop('purchased_package_id', None)

    if package_id:
        from packages.models import Package
        purchased_package = get_object_or_404(Package, id=package_id)
        profile.package = purchased_package
    else:
        purchased_package = profile.package  # fallback if already assigned

    profile.package_assigned_date = timezone.now()

    if parent_email:
        profile.parent_email = parent_email

    profile.save()
    
    if parent_email:
        send_mail(
            subject='Tutoring Package Confirmation',
            message=f"Thank you for purchasing the {purchased_package.name} package. "
                    f"Your student now has {purchased_package.num_sessions} sessions available.",
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