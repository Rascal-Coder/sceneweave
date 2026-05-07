"""Runtime configuration (env + optional .env)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    """应用配置。可通过环境变量覆盖。"""

    projects_root: Path
    database_url: str

    @staticmethod
    def from_env() -> Settings:
        root = os.environ.get("SCENEWEAVE_PROJECTS_ROOT", "").strip()
        projects_root = Path(root) if root else _REPO_ROOT / "projects"

        db_url = os.environ.get("SCENEWEAVE_DATABASE_URL", "").strip()
        if not db_url:
            data_dir = _REPO_ROOT / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            db_path = data_dir / "sceneweave.db"
            db_url = f"sqlite+aiosqlite:///{db_path.as_posix()}"

        return Settings(projects_root=projects_root, database_url=db_url)


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
