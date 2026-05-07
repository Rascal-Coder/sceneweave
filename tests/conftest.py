from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient

_REPO = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session", autouse=True)
def configure_test_env() -> None:
    tmp = tempfile.TemporaryDirectory()
    path = Path(tmp.name)
    os.environ["SCENEWEAVE_PROJECTS_ROOT"] = str(path / "projects")
    os.environ["SCENEWEAVE_DATABASE_URL"] = f"sqlite+aiosqlite:///{(path / 'sceneweave.db').as_posix()}"

    from lib.config import get_settings, reset_settings_cache

    reset_settings_cache()
    cfg = Config(str(_REPO / "alembic.ini"))
    cfg.set_main_option("sqlalchemy.url", get_settings().database_url)
    command.upgrade(cfg, "head")

    yield

    tmp.cleanup()


@pytest.fixture
async def client(configure_test_env: None) -> AsyncClient:
    from lib.config import get_settings
    from lib.db.engine import dispose_engine, init_db
    from server.app import app

    init_db(get_settings())
    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
            yield ac
    finally:
        await dispose_engine()
