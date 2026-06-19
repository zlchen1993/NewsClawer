from model.news import NewsItem

# 话题详情页链接（Discourse 路由：/t/{slug}/{id}）
_TOPIC_URL = "https://linux.do/t/{slug}/{id}"


def parse_hot_board(data: dict) -> list[NewsItem]:
    """把 Discourse top 接口 JSON 映射为 NewsItem 列表。

    结构为 {"topic_list": {"topics": [...]}}：标题取 title，热度取 views（浏览量），
    链接按 /t/{slug}/{id} 拼出，封面取 image_url。
    """
    topics: list[dict] = (data.get("topic_list") or {}).get("topics") or []

    items: list[NewsItem] = []
    rank = 0
    for t in topics:
        tid = t.get("id")
        if tid is None:
            continue
        rank += 1
        views = t.get("views")
        items.append(
            NewsItem(
                platform="linuxdo",
                news_id=str(tid),
                title=t.get("title") or "",
                url=_TOPIC_URL.format(slug=t.get("slug") or "topic", id=tid),
                rank=rank,
                hot_value=str(views) if views is not None else None,
                cover_image=t.get("image_url"),
            )
        )
    return items
