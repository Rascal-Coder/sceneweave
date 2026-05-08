"""
任务队列路由。
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from lib.generation_queue import get_generation_queue
from lib.i18n import Translator
from server.auth import CurrentUser

router = APIRouter()


def get_task_queue():
    return get_generation_queue()


@router.get("/tasks/stats")
async def get_task_stats(_user: CurrentUser, project_name: str | None = None):
    queue = get_task_queue()
    stats = await queue.get_task_stats(project_name=project_name)
    return {"stats": stats}


@router.get("/tasks")
async def list_tasks(
    _user: CurrentUser,
    project_name: str | None = None,
    status: str | None = None,
    task_type: str | None = None,
    source: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=500),
):
    queue = get_task_queue()
    return await queue.list_tasks(
        project_name=project_name,
        status=status,
        task_type=task_type,
        source=source,
        page=page,
        page_size=page_size,
    )


@router.get("/projects/{project_name}/tasks")
async def list_project_tasks(
    project_name: str,
    _user: CurrentUser,
    status: str | None = None,
    task_type: str | None = None,
    source: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=500),
):
    queue = get_task_queue()
    return await queue.list_tasks(
        project_name=project_name,
        status=status,
        task_type=task_type,
        source=source,
        page=page,
        page_size=page_size,
    )


@router.get("/tasks/{task_id}/cancel-preview")
async def cancel_preview(task_id: str, _user: CurrentUser):
    queue = get_task_queue()
    try:
        preview = await queue.get_cancel_preview(task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return preview


@router.post("/tasks/{task_id}/cancel")
async def cancel_task(task_id: str, _user: CurrentUser):
    queue = get_task_queue()
    try:
        result = await queue.cancel_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.get("/projects/{project_name}/tasks/cancel-all-preview")
async def cancel_all_preview(project_name: str, _user: CurrentUser):
    queue = get_task_queue()
    queued_count = await queue.get_cancel_all_preview(project_name)
    return {"queued_count": queued_count}


@router.post("/projects/{project_name}/tasks/cancel-all")
async def cancel_all_queued(project_name: str, _user: CurrentUser):
    queue = get_task_queue()
    result = await queue.cancel_all_queued(project_name)
    return result


@router.get("/tasks/{task_id}")
async def get_task(
    task_id: str,
    _user: CurrentUser,
    _t: Translator,
):
    queue = get_task_queue()
    task = await queue.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=_t("task_not_found", id=task_id))
    return {"task": task}
