from abc import ABC, abstractmethod

from model.news import NewsItem


class AbstractNewsStore(ABC):
    @abstractmethod
    async def save_batch(self, items: list[NewsItem]) -> None:
        """保存一批新闻条目。"""
        raise NotImplementedError
