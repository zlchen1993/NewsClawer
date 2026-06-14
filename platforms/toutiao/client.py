import httpx
from tenacity import AsyncRetrying, retry_if_exception, stop_after_attempt, wait_fixed

import config


def _is_retryable(exc: BaseException) -> bool:
    """超时 / 连接/传输错误 / 5xx 视为可重试；4xx 等不重试。"""
    if isinstance(exc, (httpx.TimeoutException, httpx.TransportError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code >= 500
    return False


class ToutiaoClient:
    """头条 HTTP 请求封装。接收一个 httpx.AsyncClient（或兼容对象）。

    每个请求在遇到超时 / 连接错误 / 5xx 时按 config.MAX_RETRY 重试，4xx 不重试。
    """

    def __init__(self, http):
        self.http = http

    async def _get(self, url: str, headers: dict):
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(config.MAX_RETRY),
            retry=retry_if_exception(_is_retryable),
            wait=wait_fixed(0),
            reraise=True,
        ):
            with attempt:
                resp = await self.http.get(url, headers=headers)
                resp.raise_for_status()
                return resp

    async def fetch_hot_board(self) -> dict:
        resp = await self._get(config.TOUTIAO_HOT_BOARD_URL, config.TOUTIAO_PC_HEADERS)
        return resp.json()

    async def fetch_search_html(self, topic_url: str) -> str:
        resp = await self._get(topic_url, config.TOUTIAO_PC_HEADERS)
        return resp.text

    async def fetch_article_info(self, gid: str) -> dict:
        url = config.TOUTIAO_ARTICLE_INFO_URL.format(gid=gid)
        resp = await self._get(url, config.TOUTIAO_MOBILE_HEADERS)
        return resp.json()
