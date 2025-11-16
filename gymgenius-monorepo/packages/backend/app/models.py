"""Database models for GymGenius."""
# flake8: noqa: F401
# pyright: reportMissingImports=false
# pylint: disable=import-error
# type: ignore
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID as PyUUID
from uuid import uuid4

if TYPE_CHECKING:
    # Static typing help — these imports will only be used by type checkers
    from sqlalchemy import (  # type: ignore  # type: ignore
        Boolean,
        DateTime,
        Float,
        ForeignKey,
        Integer,
        String,
        Text,
    )
    from sqlalchemy import Enum as SQLEnum  # type: ignore
    from sqlalchemy.dialects.postgresql import UUID as SA_UUID  # type: ignore
    from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore
else:
    try:
        from sqlalchemy import (  # type: ignore  # type: ignore
            Boolean,
            DateTime,
            Float,
            ForeignKey,
            Integer,
            String,
            Text,
        )
        from sqlalchemy import Enum as SQLEnum  # type: ignore
        from sqlalchemy.dialects.postgresql import UUID as SA_UUID  # type: ignore
        from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore
    except Exception:  # pragma: no cover
        # Lightweight fallbacks for environments where SQLAlchemy isn't installed
        Float = float
        Boolean = bool

        class _FakeDateTime:
            def __call__(self, *args, **kwargs):
                return None

        DateTime = _FakeDateTime()

        class _FakeCallable:
            def __call__(self, *args, **kwargs):
                return None

        SQLEnum = _FakeCallable()
        def _fake_foreign_key(*args, **kwargs):  # type: ignore
            return None
        ForeignKey = _fake_foreign_key
        Integer = int
        String = str
        Text = str

        class _FakeUUID:
            def __call__(self, *args, **kwargs):
                return None

        SA_UUID = _FakeUUID()
        # For runtime/analysis environment fallback, ensure Mapped is Any so
        # editor static checkers won't complain about runtime-only typing alias
        Mapped = Any

        def mapped_column(*args, **kwargs):  # type: ignore
            return None

        def relationship(*args, **kwargs):  # type: ignore
            return None

from .db import Base  # type: ignore

# Constants to avoid duplicated literals and satisfy static analysis tools
CASCADE_ALL_DELETE = "all, delete-orphan"
USERS_ID_FK = "users.id"


class UserRole(str, Enum):
    """User role enumeration."""

    CLIENT = "client"
    TRAINER = "trainer"
    NUTRITIONIST = "nutritionist"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class SubscriptionStatus(str, Enum):
    """Subscription status enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class PaymentStatus(str, Enum):
    """Payment status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = mapped_column(
        SA_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    firebase_uid = mapped_column(
        String(128), unique=True, index=True
    )
    email = mapped_column(String(255), unique=True, index=True)
    full_name = mapped_column(String(255))
    role = mapped_column(
        SQLEnum(UserRole), default=UserRole.CLIENT
    )
    phone = mapped_column(String(20), nullable=True)
    avatar_url = mapped_column(
        String(512), nullable=True
    )
    is_active = mapped_column(Boolean, default=True)
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    subscriptions = relationship(
        "Subscription", back_populates="user", cascade=CASCADE_ALL_DELETE
    )
    workouts = relationship(
        "Workout", back_populates="user", cascade=CASCADE_ALL_DELETE
    )
    meals = relationship(
        "Meal", back_populates="user", cascade=CASCADE_ALL_DELETE
    )
    payments = relationship(
        "Payment", back_populates="user", cascade=CASCADE_ALL_DELETE
    )


class Subscription(Base):
    """Subscription model."""

    __tablename__ = "subscriptions"

    id = mapped_column(
        SA_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id = mapped_column(
        ForeignKey(USERS_ID_FK, ondelete="CASCADE")
    )
    plan_name = mapped_column(String(100))
    status = mapped_column(
        SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE
    )
    start_date = mapped_column(DateTime(timezone=True))
    end_date = mapped_column(DateTime(timezone=True))
    amount = mapped_column(Float)
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="subscriptions")


class Workout(Base):
    """Workout model."""

    __tablename__ = "workouts"

    id = mapped_column(
        SA_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id = mapped_column(
        ForeignKey(USERS_ID_FK, ondelete="CASCADE")
    )
    title = mapped_column(String(255))
    description = mapped_column(Text, nullable=True)
    duration_minutes = mapped_column(Integer)
    calories_burned = mapped_column(
        Float, nullable=True
    )
    completed_at = mapped_column(DateTime(timezone=True))
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="workouts")


class Meal(Base):
    """Meal model."""

    __tablename__ = "meals"

    id = mapped_column(
        SA_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id = mapped_column(
        ForeignKey(USERS_ID_FK, ondelete="CASCADE")
    )
    meal_name = mapped_column(String(255))
    description = mapped_column(Text, nullable=True)
    calories = mapped_column(Float)
    protein_grams = mapped_column(
        Float, nullable=True
    )
    carbs_grams = mapped_column(Float, nullable=True)
    fat_grams = mapped_column(Float, nullable=True)
    consumed_at = mapped_column(DateTime(timezone=True))
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="meals")


class Payment(Base):
    """Payment model."""

    __tablename__ = "payments"

    id = mapped_column(
        SA_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id = mapped_column(
        ForeignKey(USERS_ID_FK, ondelete="CASCADE")
    )
    razorpay_order_id = mapped_column(String(100), unique=True)
    razorpay_payment_id = mapped_column(
        String(100), unique=True, nullable=True
    )
    razorpay_signature = mapped_column(
        String(255), nullable=True
    )
    amount = mapped_column(Float)
    currency = mapped_column(String(3), default="INR")
    status = mapped_column(
        SQLEnum(PaymentStatus), default=PaymentStatus.PENDING
    )
    payment_method = mapped_column(
        String(50), nullable=True
    )
    retry_count = mapped_column(Integer, default=0)
    error_message = mapped_column(Text, nullable=True)
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="payments")
