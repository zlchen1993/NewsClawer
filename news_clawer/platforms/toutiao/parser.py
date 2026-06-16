import re
from urllib.parse import urlparse

from parsel import Selector

from model.news import NewsItem
from tools.utils import unix_to_str

# 原生头条文章的 host 白名单（排除 article.zlink.toutiao.com 等外链）
_NATIVE_HOSTS = {"toutiao.com", "www.toutiao.com", "m.toutiao.com"}
_PATH_GID_RE = re.compile(r"^/(?:group|item)/(\d+)")
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
    """从搜索页 HTML 内嵌 JSON 中取第一篇原生头条文章的 gid；无则 None。

    只接受 host 在白名单内的链接，避免误取 article.zlink.toutiao.com 等外链
    （其 h5_url 参数里可能嵌入像原生文章的路径）。
    """
    for raw_url in _ARTICLE_URL_RE.findall(search_html):
        url = raw_url.replace("\\/", "/")
        parsed = urlparse(url)
        if parsed.netloc in _NATIVE_HOSTS:
            m = _PATH_GID_RE.match(parsed.path)
            if m:
                return m.group(1)
    return None


def parse_article_info(info: dict) -> dict:
    """把移动端文章 info JSON 解析为详情字段 dict。"""
    data = info.get("data") or {}
    content_html = data.get("content") or ""
    sel = Selector(text=content_html)
    text = "".join(sel.xpath("//text()").getall()).strip()
    images = sel.xpath("//img/@src").getall()
    return {
        "article_url": data.get("url"),
        "content": text,
        "author": data.get("source"),
        "publish_time": unix_to_str(data.get("publish_time")),
        "images": images,
    }
