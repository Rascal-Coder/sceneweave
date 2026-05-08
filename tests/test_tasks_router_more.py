import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from server.auth import CurrentUserInfo, get_current_user, get_current_user_flexible
from server.routers import tasks as tasks_router


class _FakeQueue:
    def __init__(self, *, task=None):
        self.task = task

    async def get_task(self, task_id):
        return self.task


class TestTasksRouterMore:
    def test_get_task_not_found(self, monkeypatch):
        monkeypatch.setattr(tasks_router, "get_task_queue", lambda: _FakeQueue(task=None))
        app = FastAPI()
        app.dependency_overrides[get_current_user] = lambda: CurrentUserInfo(id="default", sub="testuser", role="admin")
        app.dependency_overrides[get_current_user_flexible] = lambda: CurrentUserInfo(
            id="default", sub="testuser", role="admin"
        )
        app.include_router(tasks_router.router, prefix="/api/v1")

        with TestClient(app) as client:
            resp = client.get("/api/v1/tasks/missing-task")
            assert resp.status_code == 404
            assert "不存在" in resp.json()["detail"]
