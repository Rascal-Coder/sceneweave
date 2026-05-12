"""
Uvicorn 事件循环工厂（主要为 Windows + --reload / 多 worker）。
开启 reload（或 workers>1）时，uvicorn 会将 use_subprocess 设为 True，并在 Windows 上选用
SelectorEventLoop（见 uvicorn.loops.asyncio.asyncio_loop_factory）。Selector 不支持
asyncio.create_subprocess_exec，claude_agent_sdk 拉起 Claude CLI 时会 NotImplementedError，
并被包装为 CLIConnectionError。
通过 --loop server.uvicorn_loop:create_uvicorn_event_loop 在 Windows 上强制使用 ProactorEvent循环。
"""
from __future__ import annotations
import asyncio
import sys
def create_uvicorn_event_loop() -> asyncio.AbstractEventLoop:
    if sys.platform == "win32":
        return asyncio.ProactorEventLoop()
    return asyncio.new_event_loop()