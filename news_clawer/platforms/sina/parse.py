from model.news import NewsItem


def parse_hot_board(data: dict) -> list[NewsItem]:
    """把新浪新闻热榜接口 JSON 映射为 NewsItem 列表。

    结构为 {"data": {"hotList": [{"base": {...}, "info": {...}}]}}：
    标题取 info.title，热度取 info.hotValue，链接取 base.base.url，
    news_id 取 base.base.uniqueId（缺失时退回标题）。
    """
    hot: list[dict] = (data.get("data") or {}).get("hotList") or []

    items: list[NewsItem] = []
    rank = 0
    for row in hot:
        info = row.get("info") or {}
        title = info.get("title") or ""
        if not title:
            continue
        rank += 1
        base = (row.get("base") or {}).get("base") or {}
        hot_value = info.get("hotValue")
        items.append(
            NewsItem(
                platform="sina",
                news_id=str(base.get("uniqueId") or title),
                title=title,
                url=base.get("url") or "",
                rank=rank,
                hot_value=str(hot_value) if hot_value else None,
            )
        )
    return items
