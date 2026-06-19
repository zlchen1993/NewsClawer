import asyncio
import json

import config
from base.base_crawler import BrowserNewsCrawler
from model.news import NewsItem
from platforms.linuxdo.parse import parse_hot_board
from store.base import AbstractNewsStore
from tools.logger import get_logger

logger = get_logger("linuxdo")


class LinuxDoCrawler(BrowserNewsCrawler):
    """LinuxDo（Discourse 论坛）浏览器模式爬虫。

    站点受 Cloudflare 保护，普通 HTTP 会被 403，故先用浏览器访问首页通过人机
    校验，再在页内 fetch Discourse 的 top.json。匿名访问话题详情会被限流(429)，
    因此只抓热门话题列表（标题/浏览量/链接），不抓正文。
    """

    platform = "linuxdo"

    async def login(self) -> None:
        # 无需账号，但需访问首页让 Cloudflare 在后台完成校验、写入放行 cookie
        await self.page.goto(
            config.LINUXDO_HOME_URL, wait_until="domcontentloaded", timeout=60000
        )

    async def _fetch_json(self, path: str) -> dict:
        """页内 fetch 取 JSON；以能否解析出 JSON 作为 Cloudflare 通过信号，未过则轮询重试。"""
        for _ in range(config.LINUXDO_CF_WAIT_TRIES):
            raw = await self.page.evaluate(
                "async (p) => { const r = await fetch(p, {headers: {'Accept': 'application/json'}}); return await r.text(); }",
                path,
            )
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                await self.page.wait_for_timeout(1500)  # 多半仍在 Cloudflare 校验，稍后重试
        raise RuntimeError(f"linuxdo: 无法获取 {path}（Cloudflare 校验未通过？）")

    async def fetch_hot_list(self) -> list[NewsItem]:
        data = await self._fetch_json(config.LINUXDO_TOP_PATH)
        items = parse_hot_board(data)
        if config.HOT_LIST_LIMIT and config.HOT_LIST_LIMIT > 0:
            items = items[: config.HOT_LIST_LIMIT]
        return items

    async def fetch_detail(self, item: NewsItem) -> NewsItem:
        # 匿名访问话题详情会被限流(429)，列表已含标题/热度/链接，详情阶段不抓正文。
        return item


async def main():
    from store.json_store import JsonNewsStore
    crawler = LinuxDoCrawler(store=JsonNewsStore())
    await crawler.start()


if __name__ == "__main__":
    asyncio.run(main())
