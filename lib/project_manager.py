"""项目目录与 project.json 的创建、读写与删除。"""

from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from lib.config import Settings, get_settings
from lib.data_validator import ProjectId, ProjectJson, ProjectJsonPatch, validate_project_id


class ProjectError(Exception):
    """项目文件系统或校验相关错误。"""


class ProjectNotFoundError(ProjectError):
    pass


class ProjectConflictError(ProjectError):
    pass


class ProjectManager:
    """管理 projects/<project_id>/ 目录与 project.json。"""

    PROJECT_FILE = "project.json"

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    @property
    def projects_root(self) -> Path:
        return self._settings.projects_root

    def project_dir(self, project_id: str) -> Path:
        validate_project_id(project_id)
        return self.projects_root / project_id

    def project_json_path(self, project_id: str) -> Path:
        return self.project_dir(project_id) / self.PROJECT_FILE

    def exists(self, project_id: str) -> bool:
        validate_project_id(project_id)
        return self.project_json_path(project_id).is_file()

    def ensure_projects_root(self) -> None:
        self.projects_root.mkdir(parents=True, exist_ok=True)

    def create_project(self, project_id: ProjectId, name: str, description: str = "") -> ProjectJson:
        validate_project_id(project_id)
        self.ensure_projects_root()
        root = self.project_dir(project_id)
        if root.exists():
            raise ProjectConflictError(f"项目目录已存在: {project_id}")
        now = datetime.now(UTC)
        body = ProjectJson(
            id=project_id,
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
            episodes=[],
        )
        root.mkdir(parents=True, exist_ok=False)
        # 预留子目录，剧本 / 角色等后续放 JSON 或 YAML
        for sub in ("episodes", "characters", "scenes", "assets"):
            (root / sub).mkdir(exist_ok=True)
        self._write_json(project_id, body)
        return body

    def read_project_json(self, project_id: str) -> ProjectJson:
        path = self.project_json_path(project_id)
        if not path.is_file():
            raise ProjectNotFoundError(f"未找到项目: {project_id}")
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ProjectError(f"project.json 不是合法 JSON: {e}") from e
        try:
            return ProjectJson.model_validate(raw)
        except ValidationError as e:
            raise ProjectError(f"project.json 结构不合法: {e}") from e

    def write_project_json(self, project_id: str, data: ProjectJson) -> None:
        if data.id != project_id:
            raise ProjectError("project.json 内 id 与路径不一致")
        self._write_json(project_id, data)

    def _write_json(self, project_id: str, data: ProjectJson) -> None:
        path = self.project_json_path(project_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        # datetime 以 ISO 8601 写入磁盘
        payload = data.model_dump(mode="json")
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def update_metadata(self, project_id: str, patch: ProjectJsonPatch) -> ProjectJson:
        current = self.read_project_json(project_id)
        data = current.model_dump()
        updates: dict[str, Any] = patch.model_dump(exclude_unset=True)
        data.update(updates)
        data["updated_at"] = datetime.now(UTC)
        updated = ProjectJson.model_validate(data)
        self.write_project_json(project_id, updated)
        return updated

    def delete_project_tree(self, project_id: str) -> None:
        validate_project_id(project_id)
        root = self.project_dir(project_id)
        if root.is_dir():
            shutil.rmtree(root)
