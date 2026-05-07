"""project.json 结构定义与校验（Pydantic）。"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PlainValidator, field_validator

_PROJECT_ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def validate_project_id(value: str) -> str:
    if not value or len(value) > 64 or not _PROJECT_ID_RE.match(value):
        raise ValueError(
            "project id 须为小写字母、数字与连字符，长度 1–64，且不能以连字符开头或结尾"
        )
    return value


ProjectId = Annotated[str, PlainValidator(validate_project_id)]


def _ensure_utc_dt(v: object) -> datetime:
    if isinstance(v, datetime):
        if v.tzinfo is None:
            return v.replace(tzinfo=UTC)
        return v.astimezone(UTC)
    if isinstance(v, str):
        d = datetime.fromisoformat(v.replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=UTC)
        return d.astimezone(UTC)
    raise TypeError("expected datetime or iso string")


class EpisodeRef(BaseModel):
    """剧集 / 分集引用（M1 仅占位，后续可扩展文件路径等）。"""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=128)
    title: str = Field(default="", max_length=512)


class ProjectJson(BaseModel):
    """磁盘 project.json 的权威结构。"""

    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=1, ge=1, le=1)
    id: ProjectId
    name: str = Field(min_length=1, max_length=512)
    description: str = Field(default="", max_length=16_000)
    created_at: datetime
    updated_at: datetime
    episodes: list[EpisodeRef] = Field(default_factory=list)

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def _utc_datetimes(cls, v: object) -> datetime:
        return _ensure_utc_dt(v)


class ProjectJsonPatch(BaseModel):
    """PATCH 元数据时允许的字段子集。"""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=512)
    description: str | None = Field(default=None, max_length=16_000)
    episodes: list[EpisodeRef] | None = None
