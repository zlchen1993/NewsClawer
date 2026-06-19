from urllib.parse import quote

from model.news import NewsItem

# 热搜词指向微博站内搜索结果页（无独立文章正文）
_SEARCH_URL = "https://s.weibo.com/weibo?q={query}"


def parse_hot_board(data: dict) -> list[NewsItem]:
    """把微博热搜接口 JSON 映射为 NewsItem 列表。

    结构为 {"data": {"realtime": [...]}}；跳过广告项（is_ad），
    用热搜词本身作 news_id，链接指向站内搜索页。
    """
    realtime: list[dict] = (data.get("data") or {}).get("realtime") or []

    items: list[NewsItem] = []
    rank = 0
    for row in realtime:
        if row.get("is_ad"):
            continue  # 广告/推广位，非自然热搜
        word = row.get("word") or ""
        if not word:
            continue
        rank += 1
        scheme = row.get("word_scheme") or f"#{word}#"
        num = row.get("num")
        items.append(
            NewsItem(
                platform="weibo",
                news_id=word,
                title=row.get("note") or word,
                url=_SEARCH_URL.format(query=quote(scheme, safe="")),
                rank=rank,
                hot_value=str(num) if num is not None else None,
            )
        )
    return items
