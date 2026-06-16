import asyncio

import config
from base.base_crawler import HttpNewsCrawler
from model.news import NewsItem
from platforms.toutiao.client import ToutiaoClient
from platforms.toutiao.parser import (
    parse_hot_board,
    extract_article_gid,
    parse_article_info,
)
from store.base import AbstractNewsStore


class ToutiaoCrawler(HttpNewsCrawler):
    platform = "toutiao"

    def __init__(self, store: AbstractNewsStore):
        super().__init__(store)
        self.client: ToutiaoClient | None = None

    async def setup(self) -> None:
        await super().setup()          # 创建 self.http
        self.client = ToutiaoClient(self.http)

    async def fetch_hot_list(self) -> list[NewsItem]:
        data = await self.client.fetch_hot_board()
        items = parse_hot_board(data)
        if config.HOT_LIST_LIMIT and config.HOT_LIST_LIMIT > 0:
            items = items[: config.HOT_LIST_LIMIT]
        return items

    async def fetch_detail(self, item: NewsItem) -> NewsItem:
        search_html = await self.client.fetch_search_html(item.url)
        gid = extract_article_gid(search_html)
        if not gid:
            return item               # 找不到代表文章，保留列表字段
        info = await self.client.fetch_article_info(gid)
        detail = parse_article_info(info)
        item.article_url = detail["article_url"]
        item.content = detail["content"]
        item.author = detail["author"]
        item.publish_time = detail["publish_time"]
        item.images = detail["images"]
        return item


async def main():
   from store.json_store import JsonNewsStore
   clawer=ToutiaoCrawler(store=JsonNewsStore())
   await clawer.setup()
   await clawer.start()


if __name__ == '__main__':
    asyncio.run(main())
