import asyncio
from abc import ABC, abstractmethod

import httpx

import config
from model.news import NewsItem
from store.base import AbstractNewsStore
from tools.logger import get_logger

logger = get_logger("crawler")


class AbstractNewsCrawler(ABC):
    """顶层抽象：固化通用爬取流程（模板方法）。子类只填平台差异。"""

    platform: str = ""

    def __init__(self, store: AbstractNewsStore):
        self.store = store

    async def start(self) -> None:
        try:
            await self.setup()
            items = await self.fetch_hot_list()
            logger.info("[%s] 热榜抓取 %d 条", self.platform, len(items))
            if config.ENABLE_FETCH_CONTENT:
                items = await self._fetch_all_details(items)
            await self.store.save_batch(items)
            logger.info("[%s] 已存储 %d 条", self.platform, len(items))
        finally:
            await self.close()

    # 生命周期钩子：默认空实现，中间层/子类按需重写
    async def setup(self) -> None:
        pass

    async def close(self) -> None:
        pass

    @abstractmethod
    async def fetch_hot_list(self) -> list[NewsItem]:
        """请求并解析热榜，返回填好列表字段的 NewsItem。"""
        raise NotImplementedError

    @abstractmethod
    async def fetch_detail(self, item: NewsItem) -> NewsItem:
        """抓取正文，补全 content/author/publish_time/images。"""
        raise NotImplementedError

    async def _fetch_all_details(self, items: list[NewsItem]) -> list[NewsItem]:
        sem = asyncio.Semaphore(config.MAX_CONCURRENCY)

        async def _one(item: NewsItem) -> NewsItem:
            async with sem:
                try:
                    if config.REQUEST_INTERVAL:
                        await asyncio.sleep(config.REQUEST_INTERVAL)
                    return await self.fetch_detail(item)
                except Exception as e:  # 异常隔离：单条失败不影响其它
                    logger.warning("[%s] 抓正文失败 %s: %s", self.platform, item.url, e)
                    return item

        return await asyncio.gather(*[_one(i) for i in items])


class HttpNewsCrawler(AbstractNewsCrawler):
    """HTTP 抓取模式：提供共享的 httpx.AsyncClient。"""

    def __init__(self, store: AbstractNewsStore):
        super().__init__(store)
        self.http: httpx.AsyncClient | None = None

    async def setup(self) -> None:
        self.http = httpx.AsyncClient(timeout=config.REQUEST_TIMEOUT, follow_redirects=True)

    async def close(self) -> None:
        if self.http is not None:
            await self.http.aclose()
            self.http = None


class BrowserNewsCrawler(AbstractNewsCrawler):
    """浏览器抓取模式骨架：启动 playwright、加载/保存 cookie、按需登录。

    首期为骨架，持有 context/page 句柄并定义登录钩子；具体平台落地时扩展。
    """

    def __init__(self, store: AbstractNewsStore):
        super().__init__(store)
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def setup(self) -> None:
        from playwright.async_api import async_playwright
        from tools.browser import launch_context

        self.playwright = await async_playwright().start()
        self.browser, self.context = await launch_context(self.playwright, config.HEADLESS)
        self.page = await self.context.new_page()
        await self.login()

    async def close(self) -> None:
        if self.context is not None:
            await self.context.close()
        if self.browser is not None:
            await self.browser.close()
        if self.playwright is not None:
            await self.playwright.stop()

    async def login(self) -> None:
        """子类按需重写：调用对应的 AbstractLogin 实现完成登录。默认不登录。"""
        pass
