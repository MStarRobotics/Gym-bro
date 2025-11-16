"""Test configuration and fixtures."""
import asyncio
from typing import AsyncGenerator

import pytest  # type: ignore
from sqlalchemy.ext.asyncio import (  # type: ignore[import-not-found]
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings  # type: ignore[import-not-found]
from app.db import Base  # type: ignore[import-not-found]

# Test database URL
TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    "/gymgenius_dev", "/gymgenius_test"
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    test_session_local = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with test_session_local() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
def mock_firebase_user():
    """Mock Firebase user data."""
    return {
        "uid": "test-uid-123",
        "email": "test@example.com",
        "email_verified": True,
        "display_name": "Test User",
    }
