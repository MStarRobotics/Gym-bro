# flake8: noqa
# pyright: reportMissingImports=false
"""Tests for database models."""
from datetime import datetime, timezone

import pytest  # type: ignore
from app.models import (Meal, Payment, PaymentStatus, User,  # type: ignore
                        UserRole, Workout)
from sqlalchemy import select  # type: ignore
from sqlalchemy.orm import selectinload  # type: ignore


@pytest.mark.asyncio
async def test_create_user(db_session):
    """Test creating a user."""
    user = User(
        firebase_uid="test-uid-123",
        email="test@example.com",
        full_name="Test User",
        role=UserRole.CLIENT,
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.role == UserRole.CLIENT
    assert user.is_active is True


@pytest.mark.asyncio
async def test_create_workout(db_session):
    """Test creating a workout."""
    user = User(
        firebase_uid="test-uid-456",
        email="workout@example.com",
        full_name="Workout User",
        role=UserRole.CLIENT,
    )
    db_session.add(user)
    await db_session.commit()
    
    workout = Workout(
        user_id=user.id,
        title="Morning Run",
        duration_minutes=30,
        calories_burned=250.0,
        completed_at=datetime.now(timezone.utc),
    )
    
    db_session.add(workout)
    await db_session.commit()
    await db_session.refresh(workout)
    
    assert workout.id is not None
    assert workout.title == "Morning Run"
    assert workout.duration_minutes == 30


@pytest.mark.asyncio
async def test_user_workouts_relationship(db_session):
    """Test user-workouts relationship."""
    user = User(
        firebase_uid="test-uid-789",
        email="relation@example.com",
        full_name="Relation User",
        role=UserRole.CLIENT,
    )
    db_session.add(user)
    await db_session.commit()
    
    workout1 = Workout(
        user_id=user.id,
        title="Workout 1",
        duration_minutes=30,
        completed_at=datetime.now(timezone.utc),
    )
    workout2 = Workout(
        user_id=user.id,
        title="Workout 2",
        duration_minutes=45,
        completed_at=datetime.now(timezone.utc),
    )
    
    db_session.add_all([workout1, workout2])
    await db_session.commit()
    await db_session.refresh(user)

    # Pre-load relationship using selectinload to avoid greenlet/MissingGreenlet
    result = await db_session.execute(
        select(User).options(selectinload(User.workouts)).filter_by(id=user.id)
    )
    loaded_user = result.scalar_one()

    assert len(loaded_user.workouts) == 2
