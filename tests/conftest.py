import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from backend.database.base import Base
from backend.database.engine import get_session
from backend.database.models import UserModel, ProductModel, CategoryModel


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def async_engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def async_session(async_engine):
    async_session_local = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_local() as session:
        yield session


@pytest.fixture
async def client(async_session):
    async def override_get_session():
        yield async_session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(async_session):
    user = UserModel(tg_id=123456789, username="testuser", first_name="Test")
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user


@pytest.fixture
async def test_product(async_session):
    product = ProductModel(
        title="Test Knife",
        description="A test knife",
        price=99.99,
        stock=10,
        images=["https://example.com/knife.jpg"]
    )
    async_session.add(product)
    await async_session.commit()
    await async_session.refresh(product)
    return product


@pytest.fixture
async def test_category(async_session):
    category = CategoryModel(
        name="Kitchen Knives",
        slug="kitchen-knives",
        description="Professional kitchen knives"
    )
    async_session.add(category)
    await async_session.commit()
    await async_session.refresh(category)
    return category
