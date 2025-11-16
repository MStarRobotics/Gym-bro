"""Razorpay payment integration service."""
import asyncio
import hashlib
import hmac
import logging
from typing import Optional

import razorpay
from fastapi import HTTPException, status

from .config import settings
from .models import Payment
from .repository import BaseRepository

logger = logging.getLogger(__name__)


class RazorpayService:
    """Service for handling Razorpay payment operations."""

    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds

    def __init__(self):
        """Initialize Razorpay client."""
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

    async def create_order(
        self, amount: float, currency: str = "INR"
    ) -> dict:
        """Create a Razorpay order with retry logic."""
        amount_paise = int(amount * 100)  # Convert to paise

        order_data = {
            "amount": amount_paise,
            "currency": currency,
            "payment_capture": 1,  # Auto capture
        }

        for attempt in range(self.MAX_RETRIES):
            try:
                order = await asyncio.to_thread(
                    self.client.order.create, data=order_data
                )
                logger.info(f"Razorpay order created: {order['id']}")
                return order
            except Exception as e:
                logger.error(
                    f"Order creation attempt {attempt + 1} failed: {e}"
                )
                if attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(
                        self.RETRY_DELAY * (2 ** attempt)
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Payment service temporarily unavailable",
                    )

    def verify_signature(
        self,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ) -> bool:
        """Verify Razorpay payment signature."""
        message = f"{razorpay_order_id}|{razorpay_payment_id}"
        secret = settings.RAZORPAY_KEY_SECRET.encode()

        expected_signature = hmac.new(
            secret, message.encode(), hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(
            expected_signature, razorpay_signature
        )

    async def fetch_payment_details(
        self, payment_id: str
    ) -> Optional[dict]:
        """Fetch payment details from Razorpay."""
        try:
            payment = await asyncio.to_thread(
                self.client.payment.fetch, payment_id
            )
            return payment
        except Exception as e:
            logger.error(f"Failed to fetch payment details: {e}")
            return None

    async def process_payment(
        self,
        payment_repo: BaseRepository[Payment],
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ) -> Payment:
        """Process and verify payment."""
        # Verify signature
        is_valid = self.verify_signature(
            razorpay_order_id, razorpay_payment_id, razorpay_signature
        )

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payment signature",
            )

        # Fetch payment details
        payment_details = await self.fetch_payment_details(
            razorpay_payment_id
        )

        if not payment_details:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment verification failed",
            )

        # Update payment record
        # Note: This is simplified - in production, query by order_id
        # payment = await payment_repo.update(...)
        logger.info(
            f"Payment processed successfully: {razorpay_payment_id}"
        )

        return payment_details


razorpay_service = RazorpayService()
