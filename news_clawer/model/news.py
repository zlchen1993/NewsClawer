from datetime import datetime

from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


class NewsItem(BaseModel):
    """跨平台统一的新闻条目模型。

    列表阶段字段在 fetch_hot_list 填充；详情阶段字段在 fetch_detail 补全。
    """

    platform: str                       # 平台标识，如 "toutiao"
    news_id: str                        # 平台内唯一 ID
    title: str                          # 标题
    url: str                            # 热点/话题链接
    rank: int | None = None             # 热榜排名
    hot_value: str | None = None        # 热度值（原样字符串）
    cover_image: str | None = None      # 封面/缩略图

    article_url: str | None = None      # 代表文章链接（详情阶段解析）
    content: str | None = None          # 正文纯文本
    author: str | None = None           # 作者/来源
    publish_time: str | None = None     # 发布时间（原样字符串）
    images: list[str] = Field(default_factory=list)  # 正文内图片

    crawl_time: str = Field(default_factory=_now_iso)  # 抓取时间 ISO
