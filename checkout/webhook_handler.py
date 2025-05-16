from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from checkout.models import Purchase, Package
from user_profiles.models import UserProfile, Subject
import logging

logger = logging.getLogger(__name__)


class StripeWebhookHandler:
    def __init__(self, request):
        self.request = request

    def handle_payment_intent_succeeded(self, event):
        logger.info("Handling payment_intent.succeeded")
        
        intent = event['data']['object']
        metadata = intent.get('metadata', {})
        amount_charged = intent['amount_received'] / 100
        currency = intent['currency'].upper()
        payment_intent_id = intent.get('id')
        
        user_id = metadata.get('user_id')
        package_id = metadata.get('package_id')
        customer_email = metadata.get('customer_email')
        subject_name = metadata.get('subject')

        logger.debug(f"Metadata received: {metadata}")

        # Get user and package
        try:
            user = User.objects.get(id=user_id)
            package = Package.objects.get(id=package_id)
            profile = user.userprofile
        except (User.DoesNotExist, Package.DoesNotExist, UserProfile.DoesNotExist):
            logger.error("User, package, or user profile not found.")
            return HttpResponse("success")
        
        # Save subject to profile
        if subject_name:
            try:
                subject = Subject.objects.get(name=subject_name)
                profile.subjects.add(subject)
                profile.save()
                print(f"Subject '{subject.name}' saved to user profile: {user.username}")
            except Subject.DoesNotExist:
                print(f"Subject not found: {subject_name}")

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
            'amount_charged': f"{amount_charged:.2f}",
            'currency': currency,
            'subject': subject
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

        return HttpResponse("success")    

    def unhandled_event(self, event):
        print(f"Unhandled event type: {event['type']}")
        return HttpResponse(status=200)
    
    def handle_payment_intent_payment_failed(self, event):
        intent = event['data']['object']
        print("Payment failed:", intent['id'])
        return HttpResponse(status=200)
