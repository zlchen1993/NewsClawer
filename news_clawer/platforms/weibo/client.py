import config
from tools.http import get_with_retry


class WeiboClient:
    """微博热搜 HTTP 请求封装。接收一个 httpx.AsyncClient（或兼容对象）。

    每个请求经 tools.http.get_with_retry：超时 / 连接错误 / 5xx 按 config.MAX_RETRY
    重试，4xx 不重试。
    """

    def __init__(self, http):
        self.http = http

    async def fetch_hot_board(self) -> dict:
        resp = await get_with_retry(self.http, config.WB_HOT_SEARCH_URL, config.WB_PC_HEADERS)
        return resp.json()
