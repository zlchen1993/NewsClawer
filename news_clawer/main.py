import argparse
import asyncio
import io
import sys

# 强制 UTF-8，避免 Windows 终端输出中文乱码
if sys.stdout and hasattr(sys.stdout, "buffer"):
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "buffer"):
    if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import config
from base.base_crawler import AbstractNewsCrawler
from platforms.toutiao.core import ToutiaoCrawler
from platforms.tx.core import TencentCrawler
from platforms.pengpai.core import PengpaiCrawler
from platforms.weibo.core import WeiboCrawler
from platforms.sina.core import SinaCrawler
from platforms.linuxdo.core import LinuxDoCrawler
from store.base import AbstractNewsStore
from store.json_store import JsonNewsStore


def build_store() -> AbstractNewsStore:
    """按 config.SAVE_DATA_OPTION 构造存储后端。"""
    if config.SAVE_DATA_OPTION == "postgres":
        from store.postgres_store import PostgresNewsStore

        return PostgresNewsStore()
    return JsonNewsStore(data_dir=config.DATA_DIR)


class CrawlerFactory:
    CRAWLERS: dict[str, type[AbstractNewsCrawler]] = {
        "toutiao": ToutiaoCrawler,
        "tencent": TencentCrawler,
        "pengpai": PengpaiCrawler,
        "weibo": WeiboCrawler,
        "sina": SinaCrawler,
        "linuxdo": LinuxDoCrawler,
    }

    @staticmethod
    def create(platform: str, store: AbstractNewsStore | None = None) -> AbstractNewsCrawler:
        cls = CrawlerFactory.CRAWLERS.get(platform)
        if not cls:
            supported = ", ".join(sorted(CrawlerFactory.CRAWLERS))
            raise ValueError(f"不支持的平台: {platform!r}。已支持: {supported}")
        return cls(store=store if store is not None else build_store())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="多平台热点新闻爬虫")
    parser.add_argument("--platform", default=config.PLATFORM, help="目标平台")
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    crawler = CrawlerFactory.create(args.platform)
    await crawler.start()


if __name__ == "__main__":
    asyncio.run(main())
