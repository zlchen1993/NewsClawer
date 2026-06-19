import asyncio

import config
from base.base_crawler import HttpNewsCrawler
from model.news import NewsItem
from platforms.sina.client import SinaClient
from platforms.sina.parse import parse_hot_board
from store.base import AbstractNewsStore


class SinaCrawler(HttpNewsCrawler):
    platform = "sina"

    def __init__(self, store: AbstractNewsStore):
        super().__init__(store)
        self.client: SinaClient | None = None

    async def setup(self) -> None:
        await super().setup()          # 创建 self.http
        self.client = SinaClient(self.http)

    async def fetch_hot_list(self) -> list[NewsItem]:
        data = await self.client.fetch_hot_board()
        items = parse_hot_board(data)
        if config.HOT_LIST_LIMIT and config.HOT_LIST_LIMIT > 0:
            items = items[: config.HOT_LIST_LIMIT]
        return items

    async def fetch_detail(self, item: NewsItem) -> NewsItem:
        # 热榜条目指向搜索结果页，无独立文章正文，详情阶段不做额外抓取。
        return item


async def main():
    from store.json_store import JsonNewsStore
    crawler = SinaCrawler(store=JsonNewsStore())
    await crawler.start()


if __name__ == "__main__":
    asyncio.run(main())
