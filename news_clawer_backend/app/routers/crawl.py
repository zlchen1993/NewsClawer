"""手动触发爬取接口（辅助/调试用）。"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from app.schemas import CrawlAccepted
from main import CrawlerFactory  # 爬虫工厂（news_clawer 已在 sys.path）
from store.postgres_store import PostgresNewsStore

router = APIRouter(tags=["crawl"])


class CrawlRequest(BaseModel):
    platform: str


async def _run_crawl(platform: str) -> None:
    crawler = CrawlerFactory.create(platform, store=PostgresNewsStore())
    await crawler.start()


@router.post("/crawl", response_model=CrawlAccepted, status_code=202)
async def trigger_crawl(req: CrawlRequest, background: BackgroundTasks):
    if req.platform not in CrawlerFactory.CRAWLERS:
        supported = ", ".join(sorted(CrawlerFactory.CRAWLERS))
        raise HTTPException(status_code=400, detail=f"不支持的平台: {req.platform}。已支持: {supported}")
    background.add_task(_run_crawl, req.platform)
    return CrawlAccepted(status="accepted", platform=req.platform)
