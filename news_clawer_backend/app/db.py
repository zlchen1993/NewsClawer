"""后端数据库依赖：复用爬虫包 store.db 的引擎/会话，提供 FastAPI 会话依赖。"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from store.db import News, async_session, init_models  # noqa: F401 (re-export)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
