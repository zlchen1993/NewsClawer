"""只读接口：平台列表 / 热榜列表 / 详情。"""

import datetime as _dt

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import BigInteger, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import News, get_session
from app.schemas import NewsBrief, NewsDetail, NewsListResponse, PlatformInfo

router = APIRouter(tags=["news"])


@router.get("/platforms", response_model=list[PlatformInfo])
async def list_platforms(session: AsyncSession = Depends(get_session)):
    """返回有数据的平台及其最新批次日期与条数。"""
    latest_rows = (
        await session.execute(
            select(News.platform, func.max(News.batch_date)).group_by(News.platform)
        )
    ).all()

    result: list[PlatformInfo] = []
    for platform, latest_date in latest_rows:
        count = await session.scalar(
            select(func.count())
            .select_from(News)
            .where(News.platform == platform, News.batch_date == latest_date)
        )
        result.append(
            PlatformInfo(
                platform=platform,
                latest_date=latest_date.isoformat() if latest_date else None,
                count=count or 0,
            )
        )
    return result


@router.get("/news", response_model=NewsListResponse)
async def list_news(
    platform: str = Query(..., description="平台标识，如 toutiao / tencent"),
    date: _dt.date | None = Query(None, description="批次日期 YYYY-MM-DD，缺省取最新"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str = Query("rank", pattern="^(rank|hot)$"),
    session: AsyncSession = Depends(get_session),
):
    """按平台 + 日期分页查询热榜列表。"""
    target_date = date
    if target_date is None:
        target_date = await session.scalar(
            select(func.max(News.batch_date)).where(News.platform == platform)
        )

    if target_date is None:  # 该平台无任何数据
        return NewsListResponse(
            platform=platform, date=None, total=0, page=page, page_size=page_size, items=[]
        )

    base_where = (News.platform == platform, News.batch_date == target_date)
    total = await session.scalar(
        select(func.count()).select_from(News).where(*base_where)
    )

    if sort == "hot":
        order_by = cast(News.hot_value, BigInteger).desc().nullslast()
    else:
        order_by = News.rank.asc().nullslast()

    rows = (
        await session.execute(
            select(News)
            .where(*base_where)
            .order_by(order_by)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    return NewsListResponse(
        platform=platform,
        date=target_date.isoformat(),
        total=total or 0,
        page=page,
        page_size=page_size,
        items=[NewsBrief.model_validate(r) for r in rows],
    )


@router.get("/news/{news_pk}", response_model=NewsDetail)
async def get_news(news_pk: int, session: AsyncSession = Depends(get_session)):
    """按代理主键 id 查单条详情。"""
    row = await session.get(News, news_pk)
    if row is None:
        raise HTTPException(status_code=404, detail="news not found")
    return NewsDetail.model_validate(row)
