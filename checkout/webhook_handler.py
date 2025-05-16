from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from checkout.models import Purchase, Package
from user_profiles.models import UserProfile
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class StripeWebhookHandler:
    def __init__(self, request):
        self.request = request

    def handle_payment_intent_succeeded(self, event):
        print("⚡ Inside handle_payment_intent_succeeded")
        intent = event['data']['object']
        amount_charged = intent['amount_received'] / 100
        currency = intent['currency'].upper()
        metadata = intent.get('metadata', {})
        print("🔍 Metadata:", metadata)
        user_id = metadata.get('user_id')
        package_id = metadata.get('package_id')
        payment_intent_id = intent.get('id')
        customer_email = metadata.get('customer_email')

        # Get user and package
        try:
            user = User.objects.get(id=user_id)
            package = Package.objects.get(id=package_id)
            profile = user.userprofile
        except (User.DoesNotExist, Package.DoesNotExist):
            print("User or package not found.")
            return HttpResponse("success")

        # Create purchase
        expiration_date = timezone.now() + timedelta(weeks=8)
        Purchase.objects.create(
            user=user,
            package=package,
            expires_on=expiration_date,
            stripe_payment_intent=payment_intent_id,
            payment_status='paid',
        )

        # Update profile session count
        profile.total_sessions_available += package.num_sessions
        profile.save()
        
        # Prepare context for the templates
        context = {
            'package': package,
            'expiration_date': expiration_date,
        }

        # Render subject and body from templates
        subject = render_to_string('checkout/confirmation_subject.html', context).strip()
        body_html = render_to_string('checkout/confirmation_body.html', context)
        body_text = render_to_string('checkout/confirmation_body.txt', context)

        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=body_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[customer_email],
            )
            email.attach_alternative(body_html, "text/html")
            email.send()
            print(f"Email sent to {customer_email}")
        except Exception as e:
            print(f"Error sending email to {customer_email}: {e}")

    def unhandled_event(self, event):
        print(f"Unhandled event type: {event['type']}")
        return HttpResponse(status=200)
    
    def handle_payment_intent_payment_failed(self, event):
        intent = event['data']['object']
        print("Payment failed:", intent['id'])
        return HttpResponse(status=200)
