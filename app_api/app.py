import stripe
from fastapi import status
from fastapi.applications import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from starlette.responses import JSONResponse
from stripe.error import SignatureVerificationError

from core.config import settings
from core.logging import logger
from entities.schemas import Customer, CustomerSubscription, Invoice
from utils.notification import send_telegram_message
from utils.user.main import UserCRUD
from utils.user.subscription import SubscriptionCRUD

app = FastAPI()


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
    except ValueError as exc:
        logger.error(f"Error while decoding event! {exc}", exc_info=exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while decoding event",
        )
    except SignatureVerificationError as exc:
        logger.error(f"Invalid signature! {exc}", exc_info=exc)
        # Invalid signature
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Signature",
        )
    except Exception as exc:
        logger.error(f"Unhandled exception: {exc}", exc_info=exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unhandled Exception",
        )

    # Handle the event
    match event.type:
        case "customer.updated":
            _customer = event.data.object
            customer = Customer(**_customer)
            logger.info(f"Customer updated: {customer}")
            UserCRUD.update_user_via_stripe(customer=customer)

        case "customer.subscription.created":
            _subscription = event.data.object
            subscription = CustomerSubscription(**_subscription)
            logger.info(f"Customer subscription created: {subscription}")
            SubscriptionCRUD.create_subscription(subscription=subscription)
            await send_telegram_message(
                subscription.customer, "Your subscription has been created!"
            )

        case "customer.subscription.updated":
            _subscription = event.data.object
            subscription = CustomerSubscription(**_subscription)
            logger.info(f"Customer subscription updated: {subscription}")
            SubscriptionCRUD.update_subscription(subscription=subscription)
            await send_telegram_message(
                subscription.customer, "Your subscription is updated!"
            )

        case "customer.subscription.deleted":
            _subscription = event.data.object
            subscription = CustomerSubscription(**_subscription)
            logger.info(f"Customer subscription cancelled: {subscription}")
            SubscriptionCRUD.update_subscription(subscription=subscription)
            await send_telegram_message(
                subscription.customer, "Your subscription is cancelled!"
            )

        case "invoice.paid":
            _invoice = event.data.object
            invoice = Invoice(**_invoice)
            logger.info(f"Invoice paid: {invoice}")

        case other:
            logger.warning(f"Unhandled event type: {other}")


@app.on_event("startup")
async def startup_event():
    logger.critical("FastAPI App Started")


@app.on_event("shutdown")
async def startup_event():
    logger.critical("FastAPI App Stopped")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"intent": "error", "message": exc.detail, "detail": None},
    )
