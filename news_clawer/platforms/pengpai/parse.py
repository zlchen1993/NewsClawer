import json
import re

from parsel import Selector

from model.news import NewsItem

# 文章详情页链接模板（澎湃热榜条目无独立列表链接，由 contId 拼出）
_ARTICLE_URL = "https://www.thepaper.cn/newsDetail_forward_{news_id}"
# 详情页为 Next.js 应用，数据嵌在 __NEXT_DATA__ 脚本里
_NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S
)


def parse_hot_board(data: dict) -> list[NewsItem]:
    """把热榜接口 JSON 映射为 NewsItem 列表（仅列表字段）。

    结构为 {"data": {"hotNews": [...]}}；每条用 contId 作唯一 ID，
    列表无独立链接时按 contId 拼出文章详情链接。
    """
    hot: list[dict] = (data.get("data") or {}).get("hotNews") or []

    items: list[NewsItem] = []
    rank = 0
    for row in hot:
        cont_id = str(row.get("contId") or "")
        if not cont_id:
            continue
        rank += 1
        praise = row.get("praiseTimes")
        items.append(
            NewsItem(
                platform="pengpai",
                news_id=cont_id,
                title=row.get("name") or "",
                url=row.get("link") or _ARTICLE_URL.format(news_id=cont_id),
                rank=rank,
                hot_value=str(praise) if praise is not None else None,
                cover_image=row.get("pic") or row.get("sharePic"),
            )
        )
    return items


def _extract_next_data(html: str) -> dict | None:
    """从详情页 HTML 中提取 __NEXT_DATA__ 的 JSON 对象。"""
    m = _NEXT_DATA_RE.search(html)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def parse_article_detail(html: str) -> dict:
    """解析文章详情页，返回正文相关字段。

    正文位于 props.pageProps.detailData.contentDetail：content 为正文 HTML，
    author 为作者/来源，pubTime 为发布时间，images 为配图列表。
    """
    empty = {
        "article_url": None,
        "content": None,
        "author": None,
        "publish_time": None,
        "images": [],
    }
    data = _extract_next_data(html)
    if not data:
        return empty

    page_props = (data.get("props") or {}).get("pageProps") or {}
    detail = (page_props.get("detailData") or {}).get("contentDetail") or {}
    if not detail:
        return empty

    content_html = detail.get("content") or ""
    sel = Selector(text=content_html)
    # 排除 <style>/<script> 内的文本，避免把内联 CSS/JS 当成正文
    text_nodes = sel.xpath("//text()[not(ancestor::style) and not(ancestor::script)]").getall()
    content = "\n".join(t.strip() for t in text_nodes if t.strip())

    # 优先用结构化的 images 列表，缺失时回退到正文 <img>
    images = [im.get("url") for im in (detail.get("images") or []) if im.get("url")]
    if not images:
        images = sel.xpath("//img/@src").getall()

    cont_id = str(detail.get("contId") or "")
    return {
        "article_url": _ARTICLE_URL.format(news_id=cont_id) if cont_id else None,
        "content": content or None,
        "author": detail.get("author") or detail.get("source") or None,
        "publish_time": detail.get("pubTime") or None,
        "images": images,
    }
