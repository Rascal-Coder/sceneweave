"""控制台入口：供 `uv run sceneweave-api` 使用。"""

from __future__ import annotations


def main() -> None:
    import uvicorn

    uvicorn.run(
        "server.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
