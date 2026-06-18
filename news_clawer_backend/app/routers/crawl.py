"""手动触发爬取接口（辅助/调试用）。

POST /crawl：
- 不传 platform（或传 "all"）→ 触发全部已注册平台；
- 传具体 platform → 仅触发该平台。
均为后台 fire-and-forget，立即返回 202。
"""

import asyncio

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from app.schemas import CrawlAccepted
from main import CrawlerFactory  # 爬虫工厂（news_clawer 已在 sys.path）
from store.postgres_store import PostgresNewsStore

router = APIRouter(tags=["crawl"])


class CrawlRequest(BaseModel):
    platform: str | None = None  # 省略或 "all" 表示全部平台


async def _run_one(platform: str) -> None:
    crawler = CrawlerFactory.create(platform, store=PostgresNewsStore())
    await crawler.start()


async def _run_many(platforms: list[str]) -> None:
    # 各平台并发，单个失败不影响其它
    await asyncio.gather(*(_run_one(p) for p in platforms), return_exceptions=True)


@router.post("/crawl", response_model=CrawlAccepted, status_code=202)
async def trigger_crawl(req: CrawlRequest, background: BackgroundTasks):
    if req.platform is None or req.platform == "all":
        targets = sorted(CrawlerFactory.CRAWLERS)
    elif req.platform in CrawlerFactory.CRAWLERS:
        targets = [req.platform]
    else:
        supported = ", ".join(sorted(CrawlerFactory.CRAWLERS))
        raise HTTPException(
            status_code=400, detail=f"不支持的平台: {req.platform}。已支持: {supported}"
        )
    background.add_task(_run_many, targets)
    return CrawlAccepted(status="accepted", platforms=targets)
