import stripe
from fastapi.applications import FastAPI
from fastapi.requests import Request
from stripe.error import SignatureVerificationError

from core.config import settings
from utils.user.main import UserCRUD
from utils.user.subscription import SubscriptionCRUD
from entities.schemas import Customer, CustomerSubscription, Invoice

app = FastAPI()

log = print


@app.post("/stripe/webhook")
async def post_stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.stripe.webhook_secret,
        )
    except ValueError as e:
        # Invalid payload
        return e
    except SignatureVerificationError as e:
        # Invalid signature
        return e

    # Handle the event
    match event.type:
        case "customer.updated":
            _customer = event.data.object
            customer = Customer(**_customer)
            log(f"Customer updated: {customer}")
            UserCRUD.update_user_via_stripe(customer=customer)

        case "customer.subscription.created":
            _subscription = event.data.object
            subscription = CustomerSubscription(**_subscription)
            log(f"Customer subscription created: {subscription}")
            SubscriptionCRUD.create_subscription(subscription=subscription)

        case "customer.subscription.updated":
            _subscription = event.data.object
            subscription = CustomerSubscription(**_subscription)
            log(f"Customer subscription updated: {subscription}")
            SubscriptionCRUD.update_subscription(subscription=subscription)

        case "invoice.paid":
            _invoice = event.data.object
            invoice = Invoice(**_invoice)
            log(f"Invoice paid: {invoice}")

        case other:
            log(f"Unhandled event type: {other}")
