import asyncio

import config
from base.base_crawler import HttpNewsCrawler
from model.news import NewsItem
from platforms.pengpai.client import PengpaiClient
from platforms.pengpai.parse import parse_hot_board, parse_article_detail
from store.base import AbstractNewsStore


class PengpaiCrawler(HttpNewsCrawler):
    platform = "pengpai"

    def __init__(self, store: AbstractNewsStore):
        super().__init__(store)
        self.client: PengpaiClient | None = None

    async def setup(self) -> None:
        await super().setup()          # 创建 self.http
        self.client = PengpaiClient(self.http)

    async def fetch_hot_list(self) -> list[NewsItem]:
        data = await self.client.fetch_hot_board()
        items = parse_hot_board(data)
        if config.HOT_LIST_LIMIT and config.HOT_LIST_LIMIT > 0:
            items = items[: config.HOT_LIST_LIMIT]
        return items

    async def fetch_detail(self, item: NewsItem) -> NewsItem:
        html = await self.client.fetch_article_html(item.news_id)
        detail = parse_article_detail(html)
        item.article_url = detail["article_url"] or item.url
        item.content = detail["content"]
        item.author = detail["author"]
        item.publish_time = detail["publish_time"]
        item.images = detail["images"]
        return item


async def main():
    from store.json_store import JsonNewsStore
    crawler = PengpaiCrawler(store=JsonNewsStore())
    await crawler.start()


if __name__ == "__main__":
    asyncio.run(main())
