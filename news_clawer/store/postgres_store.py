"""Postgres 存储后端：把 NewsItem 批量 upsert 进 news 表。

与 JsonNewsStore 并列，由 config.SAVE_DATA_OPTION 选择。冲突键
(platform, news_id, batch_date)：同日同条更新。
"""

import datetime as _dt

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from model.news import NewsItem
from store.base import AbstractNewsStore
from store.db import News, async_session, init_models

# upsert 时需要更新的列（除冲突键与自增/入库时间外）
_UPDATE_COLS = (
    "title",
    "url",
    "rank",
    "hot_value",
    "cover_image",
    "article_url",
    "content",
    "author",
    "publish_time",
    "images",
    "crawl_time",
)


class PostgresNewsStore(AbstractNewsStore):
    def __init__(self, date_str: str | None = None):
        self.batch_date = (
            _dt.date.fromisoformat(date_str) if date_str else _dt.date.today()
        )
        self._initialized = False

    async def save_batch(self, items: list[NewsItem]) -> None:
        if not items:
            return
        if not self._initialized:
            await init_models()  # 幂等建表，便于爬虫脱离后端独立落库
            self._initialized = True

        platform = items[0].platform
        rows = []
        for item in items:
            row = item.model_dump()
            row["batch_date"] = self.batch_date
            rows.append(row)

        stmt = insert(News).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["platform", "news_id", "batch_date"],
            set_={col: getattr(stmt.excluded, col) for col in _UPDATE_COLS},
        )
        async with async_session() as session:
            # 每次抓取覆盖当天该平台的整份榜单快照：先删旧批次，避免同日多次
            # 抓取因热榜变动累积出重复名次/陈旧条目。
            await session.execute(
                delete(News).where(
                    News.platform == platform, News.batch_date == self.batch_date
                )
            )
            await session.execute(stmt)
            await session.commit()
