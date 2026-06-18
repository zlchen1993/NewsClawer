"""接口响应模型（pydantic v2，从 ORM 对象读取属性）。"""

from pydantic import BaseModel, ConfigDict


class NewsBrief(BaseModel):
    """列表项：不含正文。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    platform: str
    news_id: str
    title: str
    url: str
    rank: int | None = None
    hot_value: str | None = None
    cover_image: str | None = None
    author: str | None = None
    publish_time: str | None = None


class NewsDetail(NewsBrief):
    """详情：含正文与图片。"""

    article_url: str | None = None
    content: str | None = None
    images: list[str] = []
    crawl_time: str | None = None


class NewsListResponse(BaseModel):
    platform: str
    date: str | None
    total: int
    page: int
    page_size: int
    items: list[NewsBrief]


class PlatformInfo(BaseModel):
    platform: str
    latest_date: str | None
    count: int


class CrawlAccepted(BaseModel):
    status: str
    platforms: list[str]
