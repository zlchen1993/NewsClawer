"""跨平台共享的异步 HTTP 请求工具：带重试的 GET。

所有平台的 client 复用 get_with_retry，统一重试策略（超时/连接错误/5xx 重试，
4xx 不重试），重试次数取 config.MAX_RETRY。
"""

import httpx
from tenacity import AsyncRetrying, retry_if_exception, stop_after_attempt, wait_fixed

import config


def is_retryable(exc: BaseException) -> bool:
    """超时 / 连接/传输错误 / 5xx 视为可重试；4xx 等不重试。"""
    if isinstance(exc, (httpx.TimeoutException, httpx.TransportError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code >= 500
    return False


async def get_with_retry(http, url: str, headers: dict, *, max_retry: int | None = None):
    """对 http.get 做带重试的请求，成功时返回已 raise_for_status 的响应。

    :param http: httpx.AsyncClient（或兼容 .get() 的对象）
    :param max_retry: 重试次数；None 时取 config.MAX_RETRY（在调用时读取，便于测试覆盖）
    """
    attempts = config.MAX_RETRY if max_retry is None else max_retry
    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(attempts),
        retry=retry_if_exception(is_retryable),
        wait=wait_fixed(0),
        reraise=True,
    ):
        with attempt:
            resp = await http.get(url, headers=headers)
            resp.raise_for_status()
            return resp
