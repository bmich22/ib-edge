from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import stripe

from .webhook_handler import StripeWebhookHandler

stripe.api_key = settings.STRIPE_SECRET_KEY

@require_POST
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WH_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=webhook_secret
        )
    except ValueError:
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400)
    except Exception as e:
        return HttpResponse(f"Webhook error: {str(e)}", status=400)

    print("🔔 Received event:", event['type'])

    handler = StripeWebhookHandler(request)

    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    event_type = event['type']
    event_handler = event_map.get(event_type, handler.unhandled_event)

    try:
        print("📦 Dispatching to handler for:", event_type)
        print("🔧 Using function:", event_handler)
        response = event_handler(event)

        if isinstance(response, HttpResponse):
            return response
        else:
            print("⚠️ Handler returned None — defaulting to 200 OK")
            return HttpResponse(status=200)

    except Exception as e:
        print("❌ Error during event handling:", str(e))
        import traceback
        traceback.print_exc()
        return HttpResponse("Webhook handler error", status=400)