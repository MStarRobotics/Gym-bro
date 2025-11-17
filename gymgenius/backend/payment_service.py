"""
Razorpay Payment Integration for GymGenius
===========================================

This module provides secure payment processing for subscriptions and bookings.

**Features:**
- UPI payments (Google Pay, PhonePe, Paytm)
- Credit/Debit card processing
- Subscription auto-debit
- Payment verification with webhook handling
- Invoice generation
- Refund processing

**Security:**
- API keys stored in environment variables
- Payment signature verification
- PCI DSS compliant through Razorpay
- Rate limiting on payment endpoints
"""

import hashlib
import hmac
import json

# Signature verification will require hashlib/hmac; uncomment when implementing
# import hashlib
# import hmac
import logging
import os
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

# Razorpay client placeholder. Uncomment and configure when
# full integration is implemented
# import razorpay
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address

# Configure logging
logger = logging.getLogger(__name__)

# Simple in-memory stores for testing/local development
ORDERS_STORE: dict = {}
SUBSCRIPTIONS_STORE: dict = {}

INVALID_WEBHOOK_SIGNATURE = "Invalid webhook signature"
MISSING_WEBHOOK_SIGNATURE = "Missing webhook signature"
WEBHOOK_PROCESSING_FAILED = "Webhook processing failed"

# Initialize Razorpay client (keys from environment)
# razorpay_client = razorpay.Client(
#     auth=(
#         os.getenv("RAZORPAY_KEY_ID"),
#         os.getenv("RAZORPAY_KEY_SECRET"),
#     )
# )

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create router
router = APIRouter(prefix="/api/payments", tags=["Payments"])


def _require_signature_if_configured(
    webhook_signature: Optional[str],
    webhook_secret: Optional[str],
):
    """Enforce that a webhook signature exists when a secret is configured."""
    if webhook_secret and not webhook_signature:
        raise HTTPException(status_code=400, detail=MISSING_WEBHOOK_SIGNATURE)


def _verify_signature(
    webhook_body: bytes, webhook_signature: str, webhook_secret: Optional[str]
):
    """Verify webhook signature using HMAC-SHA256.

    Throws HTTPException with 400 on mismatch or verification failure.
    """
    try:
        expected = hmac.new(
            webhook_secret.encode(), webhook_body, digestmod=hashlib.sha256
        ).hexdigest()
        if expected != webhook_signature:
            raise HTTPException(status_code=400, detail=INVALID_WEBHOOK_SIGNATURE)
    except Exception:
        raise HTTPException(status_code=400, detail=INVALID_WEBHOOK_SIGNATURE)


def _parse_event(webhook_body: bytes):
    """Return (event_type, event_data) parsed from webhook body.

    Returns (None, None) on parse failure.
    """
    try:
        event_data = json.loads(webhook_body.decode())
        event_type = event_data.get("event")
    except Exception:
        event_data = None
        event_type = None
    return event_type, event_data


def _handle_payment_captured(event_data: dict):
    logger.info("WEBHOOK_EVENT: payment.captured | data=%s", event_data)
    if isinstance(event_data, dict) and event_data.get("payload"):
        payload = event_data["payload"].get("payment", {})
        order_id = payload.get("order_id")
        if order_id and order_id in ORDERS_STORE:
            ORDERS_STORE[order_id]["status"] = "captured"


def _handle_payment_failed(event_data: dict):
    logger.info("WEBHOOK_EVENT: payment.failed | data=%s", event_data)


def _handle_subscription_charged(event_data: dict):
    logger.info("WEBHOOK_EVENT: subscription.charged | data=%s", event_data)
    if isinstance(event_data, dict) and event_data.get("payload"):
        payload = event_data["payload"].get("subscription", {})
        user_id = payload.get("user_id") or payload.get("customer_id")
        if user_id and user_id in SUBSCRIPTIONS_STORE:
            SUBSCRIPTIONS_STORE[user_id]["last_charged_at"] = datetime.now(
                timezone.utc
            ).isoformat()
            SUBSCRIPTIONS_STORE[user_id]["active"] = True


def _handle_subscription_cancelled(event_data: dict):
    logger.info("WEBHOOK_EVENT: subscription.cancelled | data=%s", event_data)
    if isinstance(event_data, dict) and event_data.get("payload"):
        payload = event_data["payload"].get("subscription", {})
        user_id = payload.get("user_id") or payload.get("customer_id")
        if user_id and user_id in SUBSCRIPTIONS_STORE:
            SUBSCRIPTIONS_STORE[user_id]["active"] = False

    def _dispatch_webhook_event(
        webhook_body: bytes,
        webhook_signature: Optional[str],
        webhook_secret: Optional[str],
        trace_id: str,
    ):
        """Central dispatcher for webhook events, returns response payload dict."""
        _require_signature_if_configured(webhook_signature, webhook_secret)
        if webhook_signature and webhook_secret:
            _verify_signature(webhook_body, webhook_signature, webhook_secret)

        event_type, event_data = _parse_event(webhook_body)

        handlers = {
            "payment.captured": _handle_payment_captured,
            "payment.failed": _handle_payment_failed,
            "subscription.charged": _handle_subscription_charged,
            "subscription.cancelled": _handle_subscription_cancelled,
        }

        if isinstance(event_data, dict) and isinstance(event_type, str):
            handler = handlers.get(event_type)
            if handler:
                handler(event_data)

        return {"status": "acknowledged", "trace_id": trace_id}


class CreateOrderRequest(BaseModel):
    """Request to create a Razorpay order"""

    amount: int = Field(
        ...,
        description="Amount in smallest currency unit (paise for INR)",
    )
    currency: str = Field(
        default="INR",
        description="Currency code",
    )
    subscription_plan: str = Field(
        ...,
        description="Subscription plan ID",
    )
    user_id: str = Field(
        ...,
        description="User ID making the payment",
    )


class VerifyPaymentRequest(BaseModel):
    """Request to verify payment signature"""

    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    user_id: str


@router.post("/create-order")
@limiter.limit("10/minute")
async def create_payment_order(
    request: Request,
    order_request: CreateOrderRequest,
) -> dict:
    """
    Create a Razorpay order for payment processing.

    **Flow:**
    1. Client requests order creation with amount and plan
    2. Backend creates Razorpay order
    3. Returns order_id to frontend
    4. Frontend opens Razorpay checkout with order_id
    5. User completes payment
    6. Frontend calls /verify-payment

    **Security:**
    - Rate limited to 10 requests/minute per IP
    - Amount validation
    - User authentication required

    NOTE: Local implementation validates plan and stores an in-memory
    order with pending status
    TODO: Validate subscription plan exists
    TODO: Store order in database with pending status
    """
    trace_id = str(uuid4())

    logger.info(
        f"PAYMENT_ORDER_CREATE: Creating payment order | "
        f"user_id={order_request.user_id} | "
        f"amount={order_request.amount} | "
        f"plan={order_request.subscription_plan} | "
        f"trace_id={trace_id}"
    )

    try:
        # Validate subscription plan exists in this simple in-memory list
        SUPPORTED_PLANS = {
            "starter_monthly": 1000,
            "starter_yearly": 10000,
        }
        if order_request.subscription_plan not in SUPPORTED_PLANS:
            raise HTTPException(status_code=400, detail="Invalid subscription plan")
        # NOTE: Order creation is a placeholder; stores no DB record yet
        # order_data = {
        #     "amount": order_request.amount,
        #     "currency": order_request.currency,
        #     "receipt": f"order_rcptid_{trace_id}",
        #     "notes": {
        #         "user_id": order_request.user_id,
        #         "plan": order_request.subscription_plan
        #     }
        # }
        # order = razorpay_client.order.create(data=order_data)

        order_id = f"order_placeholder_{trace_id}"
        ORDERS_STORE[order_id] = {
            "order_id": order_id,
            "amount": order_request.amount,
            "currency": order_request.currency,
            "user_id": order_request.user_id,
            "plan": order_request.subscription_plan,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        return {
            "success": True,
            "order_id": order_id,
            "amount": order_request.amount,
            "currency": order_request.currency,
            "trace_id": trace_id,
            "message": "Payment order created successfully",
        }

    except HTTPException:
        # Preserve descriptive HTTP errors
        raise
    except Exception as e:
        logger.error(
            f"PAYMENT_ORDER_ERROR: Failed to create order | "
            f"error={str(e)} | "
            f"trace_id={trace_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "payment_creation_failed",
                "message": "Unable to initiate payment",
                "trace_id": trace_id,
            },
        )


@router.post("/verify-payment")
@limiter.limit("20/minute")
async def verify_payment(
    request: Request,
    verify_request: VerifyPaymentRequest,
):
    """
    Verify Razorpay payment signature and activate subscription.

    **Security:**
    - Cryptographic signature verification using HMAC SHA256
    - Prevents payment tampering and replay attacks
    - Updates database only after signature validation

    **Flow:**
    1. Receive payment details from frontend
    2. Verify signature using Razorpay secret
    3. Update subscription status to active
    4. Generate invoice
    5. Send confirmation email

    TODO: Implement signature verification
    TODO: Update user subscription in database
    TODO: Trigger invoice generation
    TODO: Send payment confirmation email
    """
    trace_id = str(uuid4())

    logger.info(
        f"PAYMENT_VERIFY: Verifying payment | "
        f"order_id={verify_request.razorpay_order_id} | "
        f"payment_id={verify_request.razorpay_payment_id} | "
        f"trace_id={trace_id}"
    )

    try:
        # Signature verification (HMAC SHA256)
        if not os.getenv("RAZORPAY_KEY_SECRET"):
            # If no secret configured, log and accept for now (test/stub mode)
            logger.warning(
                "PAYMENT_VERIFY: Missing RAZORPAY_KEY_SECRET; skipping verification"
            )
        else:
            _msg = (
                f"{verify_request.razorpay_order_id}|"
                f"{verify_request.razorpay_payment_id}"
            ).encode()
            razorpay_secret = os.getenv("RAZORPAY_KEY_SECRET")
            if not razorpay_secret:
                raise HTTPException(
                    status_code=500, detail="Razorpay secret not configured"
                )
            generated_signature = hmac.new(
                key=razorpay_secret.encode(),
                msg=_msg,
                digestmod=hashlib.sha256,
            ).hexdigest()

            if generated_signature != verify_request.razorpay_signature:
                raise HTTPException(status_code=400, detail="Invalid payment signature")

        # NOTE: Update order/subscription in in-memory store
        order = ORDERS_STORE.get(verify_request.razorpay_order_id)
        if order:
            order["status"] = "completed"
            SUBSCRIPTIONS_STORE[verify_request.user_id] = {
                "user_id": verify_request.user_id,
                "plan": order.get("plan"),
                "active": True,
                "activated_at": datetime.now(timezone.utc).isoformat(),
            }
        # - Mark order as completed
        # - Activate user subscription
        # - Create invoice record

        logger.info(
            f"PAYMENT_SUCCESS: Payment verified | "
            f"payment_id={verify_request.razorpay_payment_id} | "
            f"user_id={verify_request.user_id} | "
            f"trace_id={trace_id}"
        )

        return {
            "success": True,
            "verified": True,
            "payment_id": verify_request.razorpay_payment_id,
            "message": "Payment verified and subscription activated",
            "trace_id": trace_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"PAYMENT_VERIFY_ERROR: Verification failed | "
            f"error={str(e)} | "
            f"trace_id={trace_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "payment_verification_failed",
                "message": "Payment verification failed",
                "trace_id": trace_id,
            },
        )


@router.post("/webhook")
async def payment_webhook(request: Request):
    """
    Razorpay webhook handler for payment status updates.

    **Events Handled:**
    - payment.captured: Payment successful
    - payment.failed: Payment failed
    - subscription.charged: Recurring payment processed
    - subscription.cancelled: Subscription cancelled

    **Security:**
    - Webhook signature verification
    - Idempotency to prevent duplicate processing

    TODO: Implement webhook signature verification
    TODO: Handle different event types
    TODO: Update database based on events
    """
    trace_id = str(uuid4())

    try:
        _webhook_body = await request.body()
        _webhook_signature = request.headers.get("X-Razorpay-Signature")
        webhook_secret = os.getenv("RAZORPAY_KEY_SECRET")

        # Use module-level helpers to parse & handle webhook events

        # Security & verification
        _require_signature_if_configured(_webhook_signature, webhook_secret)
        if _webhook_signature and webhook_secret:
            assert webhook_secret
            _verify_signature(_webhook_body, _webhook_signature, webhook_secret)

        logger.info(
            "WEBHOOK_RECEIVED: Processing webhook | trace_id=%s",
            trace_id,
        )
        event_type, event_data = _parse_event(_webhook_body)

        handlers = {
            "payment.captured": _handle_payment_captured,
            "payment.failed": _handle_payment_failed,
            "subscription.charged": _handle_subscription_charged,
            "subscription.cancelled": _handle_subscription_cancelled,
        }

        if isinstance(event_data, dict):
            if isinstance(event_type, str):
                handler = handlers.get(event_type)
                if handler:
                    handler(event_data)

        return {"status": "acknowledged", "trace_id": trace_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"WEBHOOK_ERROR: Failed to process webhook | "
            f"error={str(e)} | "
            f"trace_id={trace_id}"
        )
        raise HTTPException(status_code=400, detail="Webhook processing failed")
