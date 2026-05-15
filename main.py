import logging
from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager
from alembic.config import Config
from alembic import command

from backend.api.routers import users, products
from backend.database.engine import engine
from backend.database.base import Base

from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

def run_migrations():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()  # запускается при старте
    yield

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
    return {"status": "ok", "api": "running"}

import traceback
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()}
    )


if __name__ == '__main__':
    import os

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)