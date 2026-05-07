"""仅存放跨请求、可索引的注册信息。业务元数据以磁盘 project.json 为准。"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from lib.db.base import Base


class ProjectRow(Base):
    """
    项目注册表：与磁盘目录一一对应。

    取舍：不缓存 name/description，避免与 project.json 双写；列表/详情从磁盘读出展示字段。
    该表用于后续任务、配额等外键关联，以及快速判断 id 是否已登记。
    """

    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
