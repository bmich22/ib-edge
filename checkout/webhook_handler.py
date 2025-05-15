from django.http import HttpResponse


class StripeWebhookHandler:
    """Handle Stripe Webhooks"""

    def payment_succeeded(self, event):
        payment_intent = event["data"]["object"]
        print(f"PaymentIntent succeeded: {payment_intent['id']}")
        # You can match this to your Order model here later
        return HttpResponse(status=200)

    def unhandled_event(self, event):
        print(f"Unhandled event type: {event['type']}")
        return HttpResponse(status=200)
