"""共享的数据库层：SQLAlchemy 异步引擎 + News ORM 模型。

写端（PostgresNewsStore）与读端（news_clawer_backend）共用这一份定义，避免表结构
分叉。DATABASE_URL 从仓库根 .env 读取（python-dotenv），缺省指向本地实例。
"""

import datetime as _dt
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    Integer,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 从仓库根（本文件的上 3 层：store -> news_clawer -> 仓库根）加载 .env
_REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_REPO_ROOT / ".env")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://admin:123456@192.168.92.100:15432/newsclawer",
)


class Base(DeclarativeBase):
    pass


class News(Base):
    __tablename__ = "news"
    __table_args__ = (
        UniqueConstraint("platform", "news_id", "batch_date", name="uq_news_platform_newsid_date"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    platform: Mapped[str] = mapped_column(Text, index=True)
    news_id: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text, default="")
    url: Mapped[str] = mapped_column(Text, default="")
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hot_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    cover_image: Mapped[str | None] = mapped_column(Text, nullable=True)
    article_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    author: Mapped[str | None] = mapped_column(Text, nullable=True)
    publish_time: Mapped[str | None] = mapped_column(Text, nullable=True)
    images: Mapped[list] = mapped_column(JSONB, default=list)
    crawl_time: Mapped[str | None] = mapped_column(Text, nullable=True)
    batch_date: Mapped[_dt.date] = mapped_column(Date, index=True)
    created_at: Mapped[_dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_models() -> None:
    """建表（幂等）。后端启动与爬虫首次落库前调用。"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
