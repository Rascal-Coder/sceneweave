from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lib.config import get_settings, reset_settings_cache
from lib.db.engine import dispose_engine, init_db
from server.routers import projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    reset_settings_cache()
    init_db(get_settings())
    yield
    await dispose_engine()


app = FastAPI(title="SceneWeave API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9999",
        "http://127.0.0.1:9999",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/v1")


@app.get("/api/v1/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
