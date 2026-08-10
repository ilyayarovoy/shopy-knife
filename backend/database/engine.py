from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
import os

load_dotenv()

raw_url = os.getenv('DATABASE_URL', '')

DATABASE_URL = raw_url.replace('postgresql://', 'postgresql+asyncpg://').split('?')[0]

engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
    connect_args={
        "ssl": "require",
        "statement_cache_size": 0,
    },
)

session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session():
    async with session_maker() as session:
        yield session