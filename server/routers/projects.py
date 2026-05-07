from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lib.data_validator import ProjectJsonPatch, validate_project_id
from lib.db.models import ProjectRow
from lib.project_manager import (
    ProjectConflictError,
    ProjectError,
    ProjectManager,
    ProjectNotFoundError,
)
from server.deps import get_db

router = APIRouter(prefix="/projects", tags=["projects"])


class ProjectCreateBody(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(..., min_length=1, max_length=64, description="URL 安全的小写 slug")
    name: str = Field(..., min_length=1, max_length=512)
    description: str = Field(default="", max_length=16_000)


class ProjectSummaryResponse(BaseModel):
    id: str
    name: str
    description: str
    created_at: str
    updated_at: str


def _manager() -> ProjectManager:
    return ProjectManager()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_project(body: ProjectCreateBody, session: AsyncSession = Depends(get_db)) -> dict:
    try:
        validate_project_id(body.id)
    except ValueError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e

    existing = await session.get(ProjectRow, body.id)
    if existing is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="项目 id 已在数据库中注册")

    pm = _manager()
    if pm.exists(body.id):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="项目目录已存在")

    try:
        doc = pm.create_project(body.id, name=body.name, description=body.description)
    except ProjectConflictError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ProjectError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    session.add(ProjectRow(id=body.id))
    try:
        await session.commit()
    except Exception:
        pm.delete_project_tree(body.id)
        await session.rollback()
        raise

    return doc.model_dump(mode="json")


@router.get("", response_model=list[ProjectSummaryResponse])
async def list_projects(session: AsyncSession = Depends(get_db)) -> list[ProjectSummaryResponse]:
    pm = _manager()
    result = await session.scalars(select(ProjectRow).order_by(ProjectRow.created_at.desc()))
    rows = list(result.all())
    out: list[ProjectSummaryResponse] = []
    for row in rows:
        try:
            doc = pm.read_project_json(row.id)
        except ProjectNotFoundError:
            continue
        except ProjectError:
            continue
        out.append(
            ProjectSummaryResponse(
                id=doc.id,
                name=doc.name,
                description=doc.description,
                created_at=doc.created_at.isoformat(),
                updated_at=doc.updated_at.isoformat(),
            )
        )
    return out


@router.get("/{project_id}")
async def get_project(project_id: str, session: AsyncSession = Depends(get_db)) -> dict:
    try:
        validate_project_id(project_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e

    row = await session.get(ProjectRow, project_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="项目未注册")

    pm = _manager()
    try:
        doc = pm.read_project_json(project_id)
    except ProjectNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="项目目录或 project.json 不存在") from None
    except ProjectError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e

    return doc.model_dump(mode="json")


@router.patch("/{project_id}")
async def patch_project(
    project_id: str,
    patch: ProjectJsonPatch,
    session: AsyncSession = Depends(get_db),
) -> dict:
    try:
        validate_project_id(project_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e

    row = await session.get(ProjectRow, project_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="项目未注册")

    pm = _manager()
    try:
        doc = pm.update_metadata(project_id, patch)
    except ProjectNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="项目不存在") from None
    except ProjectError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e

    row.updated_at = datetime.now(UTC)

    return doc.model_dump(mode="json")


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str, session: AsyncSession = Depends(get_db)) -> None:
    try:
        validate_project_id(project_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e

    row = await session.get(ProjectRow, project_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="项目未注册")

    pm = _manager()
    pm.delete_project_tree(project_id)
    await session.delete(row)
