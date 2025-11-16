"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from .models import PaymentStatus, SubscriptionStatus, UserRole


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)


class UserCreate(UserBase):
    """Schema for creating a user."""

    firebase_uid: str = Field(..., min_length=1, max_length=128)
    role: UserRole = UserRole.CLIENT


class UserResponse(UserBase):
    """Schema for user response."""

    id: UUID
    firebase_uid: str
    role: UserRole
    avatar_url: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Subscription Schemas
class SubscriptionBase(BaseModel):
    """Base subscription schema."""

    plan_name: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    start_date: datetime
    end_date: datetime


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a subscription."""

    user_id: UUID


class SubscriptionResponse(SubscriptionBase):
    """Schema for subscription response."""

    id: UUID
    user_id: UUID
    status: SubscriptionStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Workout Schemas
class WorkoutBase(BaseModel):
    """Base workout schema."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    duration_minutes: int = Field(..., gt=0)
    calories_burned: Optional[float] = Field(None, ge=0)
    completed_at: datetime


class WorkoutCreate(WorkoutBase):
    """Schema for creating a workout."""

    user_id: UUID


class WorkoutResponse(WorkoutBase):
    """Schema for workout response."""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Meal Schemas
class MealBase(BaseModel):
    """Base meal schema."""

    meal_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    calories: float = Field(..., ge=0)
    protein_grams: Optional[float] = Field(None, ge=0)
    carbs_grams: Optional[float] = Field(None, ge=0)
    fat_grams: Optional[float] = Field(None, ge=0)
    consumed_at: datetime


class MealCreate(MealBase):
    """Schema for creating a meal."""

    user_id: UUID


class MealResponse(MealBase):
    """Schema for meal response."""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Payment Schemas
class PaymentOrderCreate(BaseModel):
    """Schema for creating a payment order."""

    amount: float = Field(..., gt=0)
    currency: str = Field(default="INR", max_length=3)


class PaymentOrderResponse(BaseModel):
    """Schema for payment order response."""

    id: UUID
    razorpay_order_id: str
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime


class PaymentVerification(BaseModel):
    """Schema for payment verification."""

    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class PaymentResponse(BaseModel):
    """Schema for payment response."""

    id: UUID
    user_id: UUID
    razorpay_order_id: str
    razorpay_payment_id: Optional[str]
    amount: float
    currency: str
    status: PaymentStatus
    payment_method: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# AI Chat Schemas
class ChatRequest(BaseModel):
    """Schema for AI chat request."""

    message: str = Field(..., min_length=1, max_length=5000)
    context: Optional[str] = Field(None, max_length=10000)


class ChatResponse(BaseModel):
    """Schema for AI chat response."""

    response: str
    model: str
    tokens_used: Optional[int] = None
