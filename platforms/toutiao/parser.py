import re

from parsel import Selector

from model.news import NewsItem
from tools.utils import unix_to_str

# 匹配原生头条文章链接里的 gid：toutiao.com/group/<id>/ 或 toutiao.com/item/<id>/
_NATIVE_ARTICLE_RE = re.compile(r"toutiao\.com/(?:group|item)/(\d+)")
_ARTICLE_URL_RE = re.compile(r'"article_url"\s*:\s*"([^"]+)"')


def parse_hot_board(data: dict) -> list[NewsItem]:
    """把热榜接口 JSON 映射为 NewsItem 列表（仅列表字段）。"""
    items: list[NewsItem] = []
    for idx, row in enumerate(data.get("data", []) or [], start=1):
        image = row.get("Image") or {}
        cover = image.get("url") or image.get("uri")
        items.append(
            NewsItem(
                platform="toutiao",
                news_id=str(row.get("ClusterIdStr") or row.get("ClusterId") or ""),
                title=row.get("Title") or "",
                url=row.get("Url") or "",
                rank=idx,
                hot_value=str(row["HotValue"]) if row.get("HotValue") is not None else None,
                cover_image=cover,
            )
        )
    return items


def extract_article_gid(search_html: str) -> str | None:
    """从搜索页 HTML 内嵌 JSON 中取第一篇原生头条文章的 gid；无则 None。"""
    for raw_url in _ARTICLE_URL_RE.findall(search_html):
        url = raw_url.replace("\\/", "/")
        m = _NATIVE_ARTICLE_RE.search(url)
        if m:
            return m.group(1)
    return None


def parse_article_info(info: dict) -> dict:
    """把移动端文章 info JSON 解析为详情字段 dict。"""
    data = info.get("data") or {}
    content_html = data.get("content") or ""
    sel = Selector(text=content_html) if content_html else Selector(text="")
    text = "".join(sel.xpath("//text()").getall()).strip()
    images = sel.xpath("//img/@src").getall()
    return {
        "article_url": data.get("url"),
        "content": text,
        "author": data.get("source"),
        "publish_time": unix_to_str(data.get("publish_time")),
        "images": images,
    }
