import json

from parsel import Selector

from model.news import NewsItem


def _first(*values):
    """返回第一个非空值。"""
    for v in values:
        if v:
            return v
    return None


def parse_hot_board(data: dict) -> list[NewsItem]:
    """把热榜接口 JSON 映射为 NewsItem 列表（仅列表字段）。

    结构为 {"idlist": [{"newslist": [...]}]}；首条通常是占位提示项（无 surl），跳过。
    """
    newslist: list[dict] = []
    for group in data.get("idlist") or []:
        newslist.extend(group.get("newslist") or [])

    items: list[NewsItem] = []
    rank = 0
    for row in newslist:
        url = row.get("surl") or row.get("url")
        if not url:
            continue  # 占位提示项（如 "腾讯新闻用户最关注的热点..."）无正文链接
        rank += 1
        hot_event = row.get("hotEvent") or {}
        hot_score = hot_event.get("hotScore")
        cover = _first(
            (row.get("bigImage") or [None])[0],
            (row.get("thumbnails_qqnews") or [None])[0],
            (row.get("thumbnails") or [None])[0],
        )
        items.append(
            NewsItem(
                platform="tencent",
                news_id=str(row.get("id") or ""),
                title=row.get("title") or "",
                url=url,
                rank=rank,
                hot_value=str(hot_score) if hot_score is not None else None,
                cover_image=cover,
            )
        )
    return items


def _extract_window_data(html: str) -> dict | None:
    """从文章详情页 HTML 中提取 window.DATA 的 JSON 对象（按花括号配对截取）。"""
    marker = html.find("window.DATA")
    if marker == -1:
        return None
    start = html.find("{", marker)
    if start == -1:
        return None
    depth = 0
    in_str = False
    escaped = False
    for i in range(start, len(html)):
        c = html[i]
        if escaped:
            escaped = False
            continue
        if c == "\\":
            escaped = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(html[start : i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def parse_article_detail(html: str) -> dict:
    """解析文章详情页，返回正文相关字段。

    正文 HTML 位于 window.DATA.originContent.text；作者取 media，发布时间取 pubtime。
    """
    empty = {
        "article_url": None,
        "content": None,
        "author": None,
        "publish_time": None,
        "images": [],
    }
    data = _extract_window_data(html)
    if not data:
        return empty

    origin = data.get("originContent") or {}
    text_html = origin.get("text") or ""
    sel = Selector(text=text_html)
    content = "\n".join(t.strip() for t in sel.xpath("//text()").getall() if t.strip())
    images = sel.xpath("//img/@src").getall() + sel.xpath("//img/@data-src").getall()

    return {
        "article_url": data.get("url") or None,
        "content": content or None,
        "author": data.get("media") or None,
        "publish_time": data.get("pubtime") or None,
        "images": images,
    }
