from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from checkout.models import Purchase, Package
from user_profiles.models import UserProfile


class StripeWebhookHandler:
    def __init__(self, request):
        self.request = request
    
    """Handle Stripe Webhooks"""

    def handle_payment_intent_succeeded(self, event):
        intent = event['data']['object']
        metadata = intent.get('metadata', {})
        user_id = metadata.get('user_id')
        package_id = metadata.get('package_id')
        payment_intent_id = intent.get('id')
        customer_email = intent.get('charges', {}).get('data', [{}])[0].get('billing_details', {}).get('email')

        print(f"✅ PaymentIntent succeeded: {payment_intent_id}")

        # Get user and package
        try:
            user = User.objects.get(id=user_id)
            package = Package.objects.get(id=package_id)
            profile = user.userprofile
        except (User.DoesNotExist, Package.DoesNotExist):
            print("⚠️ User or package not found.")
            return HttpResponse(status=400)

        # Avoid duplicate purchases
        if Purchase.objects.filter(stripe_payment_intent=payment_intent_id).exists():
            print("🔁 Purchase already recorded.")
            return HttpResponse(status=200)

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

        # Send confirmation email
        subject = "Tutoring Package Confirmation – IB Edge"
        message = (
            f"Thank you for purchasing the {package.name} package!\n\n"
            f"{package.num_sessions} sessions have been added to your profile.\n"
            f"Sessions are valid until {expiration_date.strftime('%B %d, %Y')}.\n\n"
            f"If you have any questions, feel free to reply to this email.\n\n"
            f"– The IB Edge Team"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email],
            fail_silently=False,
        )

        print("📧 Confirmation email sent.")
        return HttpResponse(status=200)

    def payment_succeeded(self, event):
        payment_intent = event["data"]["object"]
        print(f"PaymentIntent succeeded: {payment_intent['id']}")
        # You can match this to your Order model here later
        return HttpResponse(status=200)

    def unhandled_event(self, event):
        print(f"Unhandled event type: {event['type']}")
        return HttpResponse(status=200)
    
    def handle_payment_intent_payment_failed(self, event):
        intent = event['data']['object']
        print("Payment failed:", intent['id'])
        return HttpResponse(status=200)
