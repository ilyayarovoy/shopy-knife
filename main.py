import logging
import asyncio
from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager

# from app.config import settings
# from app.bot import bot, dp
from backend.api.routers import users, products
from backend.database.engine import engine
from backend.database.base import Base

from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


async def init_db():
    """Инициализация БД при старте"""
    async with engine.begin() as conn:
        # Создаём все таблицы
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database initialized")

app = FastAPI(title="AI Psychologist API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api")
app.include_router(products.router, prefix="/api")


@app.get("/")
async def root():
    return {"status": "ok", "bot": "active", "api": "running"}


if __name__ == '__main__':
    import os

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)