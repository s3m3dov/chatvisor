import stripe
from fastapi.applications import FastAPI
from fastapi.requests import Request
from stripe.error import SignatureVerificationError

from core.config import settings

app = FastAPI()

log = print


@app.post("/stripe/webhook")
async def post_stripe_webhook(request: Request):
    event = None
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.stripe_webhook_secret,
        )
    except ValueError as e:
        # Invalid payload
        return e
    except SignatureVerificationError as e:
        # Invalid signature
        return e

    # Handle the event
    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object
        log("PaymentIntent was successful!")
    elif event.type == "payment_method.attached":
        payment_method = event.data.object
        log("PaymentMethod was attached to a Customer!")
    # ... handle other event types
    else:
        log(f"Unhandled event type {event.type}")
