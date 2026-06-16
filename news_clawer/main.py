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
from store.json_store import JsonNewsStore


class CrawlerFactory:
    CRAWLERS: dict[str, type[AbstractNewsCrawler]] = {
        "toutiao": ToutiaoCrawler,
        "tencent": TencentCrawler,
    }

    @staticmethod
    def create(platform: str) -> AbstractNewsCrawler:
        cls = CrawlerFactory.CRAWLERS.get(platform)
        if not cls:
            supported = ", ".join(sorted(CrawlerFactory.CRAWLERS))
            raise ValueError(f"不支持的平台: {platform!r}。已支持: {supported}")
        return cls(store=JsonNewsStore(data_dir=config.DATA_DIR))


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
