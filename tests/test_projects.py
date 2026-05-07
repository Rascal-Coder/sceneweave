from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_project_writes_disk(client: AsyncClient) -> None:
    pid = f"novel-{uuid.uuid4().hex[:10]}"
    r = await client.post(
        "/api/v1/projects",
        json={"id": pid, "name": "Novel A", "description": "desc"},
    )
    assert r.status_code == 201, r.text
    root = Path(os.environ["SCENEWEAVE_PROJECTS_ROOT"]) / pid
    assert (root / "project.json").is_file()
    assert (root / "episodes").is_dir()
    data = json.loads((root / "project.json").read_text(encoding="utf-8"))
    assert data["id"] == pid
    assert data["name"] == "Novel A"


@pytest.mark.asyncio
async def test_invalid_patch_rejected(client: AsyncClient) -> None:
    pid = f"bad-{uuid.uuid4().hex[:10]}"
    c = await client.post("/api/v1/projects", json={"id": pid, "name": "x", "description": ""})
    assert c.status_code == 201
    r = await client.patch(f"/api/v1/projects/{pid}", json={"name": ""})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_list_projects(client: AsyncClient) -> None:
    pid = f"list-{uuid.uuid4().hex[:10]}"
    await client.post("/api/v1/projects", json={"id": pid, "name": "listed", "description": ""})
    r = await client.get("/api/v1/projects")
    assert r.status_code == 200
    rows = r.json()
    assert any(p["id"] == pid for p in rows)
