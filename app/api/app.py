import stripe
from fastapi.applications import FastAPI
from fastapi.requests import Request
from stripe.error import SignatureVerificationError

from core.config import settings
from core.entities.schemas import Customer, CustomerSubscription, Invoice

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
    if event.type == "customer.created":
        _customer = event.data.object
        customer = Customer(**_customer)
        log(f"Customer created: {customer}")

    elif event.type == "customer.updated":
        _customer = event.data.object
        customer = Customer(**_customer)
        log(f"Customer updated: {customer}")

    elif event.type == "customer.subscription.created":
        _subscription = event.data.object
        subscription = CustomerSubscription(**_subscription)
        log(f"Customer subscription created: {subscription}")

    elif event.type == "customer.subscription.updated":
        _subscription = event.data.object
        subscription = CustomerSubscription(**_subscription)
        log(f"Customer subscription updated: {subscription}")

    elif event.type == "invoice.paid":
        _invoice = event.data.object
        invoice = Invoice(**_invoice)
        log(f"Invoice paid: {invoice}")

    # ... handle other event types
    else:
        log(f"Unhandled event type {event.type}")
