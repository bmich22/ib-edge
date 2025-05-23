from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from checkout.models import Purchase, Package
from user_profiles.models import Subject

User = get_user_model()


class StripeWebhookHandler:
    def __init__(self, request):
        self.request = request

    def handle_payment_intent_succeeded(self, event):
        intent = event['data']['object']
        metadata = intent.get('metadata', {})

        try:
            user_id = metadata.get('user_id')
            package_id = metadata.get('package_id')
            subject = metadata.get('subject')
            customer_email = metadata.get('customer_email')
            
            stripe_checkout_id = intent.get('id')
            stripe_payment_intent = intent.get('id')

            user = User.objects.get(id=user_id)
            profile = user.userprofile
            package = Package.objects.get(id=package_id)

            subject_id = metadata.get('subject_id')
            subject_choice = Subject.objects.get(id=subject_id)

            if not all([user_id, package_id, subject_id, customer_email]):
                return HttpResponse("Missing metadata", status=200)

            if not Purchase.objects.filter(stripe_payment_intent=stripe_payment_intent).exists():
                    purchase = Purchase.objects.create(
                    user=user,
                    package=package,
                    customer_email=customer_email,
                    subject_choice=subject_choice,
                    expires_on=timezone.now() + timezone.timedelta(weeks=8),
                    stripe_checkout_id=stripe_checkout_id,
                    stripe_payment_intent=stripe_payment_intent,
                    payment_status='paid',
                )
                    try:
                        profile.total_sessions_available += package.num_sessions
                        profile.save()
                        profile.subjects.add(subject_choice)
                        profile.total_sessions_available
                    except Exception as e:
                        print(f"Failed to update profile session count: {e}")

        except Exception as e:
            import traceback
            traceback.print_exc()
            return HttpResponse(f"Webhook \
                                processing error: {str(e)}", status=400)

        amount_charged = int(intent['amount_received']) / 100
        currency = intent['currency']
        expiration_date = timezone.now() + timezone.timedelta(weeks=8)

        context = {
            'package': package,
            'expiration_date': expiration_date,
            'amount_charged': f"{amount_charged:.2f}",
            'currency': currency.upper(),
            'subject': subject
        }

        subject = render_to_string(
            'checkout/confirmation_subject.html', context).strip()
        body_html = render_to_string(
            'checkout/confirmation_body.html', context)
        body_text = render_to_string(
            'checkout/confirmation_body.txt', context)

        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=body_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[customer_email],
            )
            email.attach_alternative(body_html, "text/html")
            email.send()
        except Exception as e:
            print(f"Error sending email to {customer_email}: {e}")

        return HttpResponse("success")

    def handle_checkout_session_completed(self, event):
        return HttpResponse("ignored")

    def unhandled_event(self, event):
        print(f"Unhandled event type: {event['type']}")
        return HttpResponse(status=200)

    def handle_payment_intent_payment_failed(self, event):
        intent = event['data']['object']
        print("Payment failed:", intent['id'])
        return HttpResponse(status=200)
