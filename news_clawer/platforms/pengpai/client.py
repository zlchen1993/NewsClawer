import config
from tools.http import get_with_retry


class PengpaiClient:
    """澎湃新闻 HTTP 请求封装。接收一个 httpx.AsyncClient（或兼容对象）。

    每个请求经 tools.http.get_with_retry：超时 / 连接错误 / 5xx 按 config.MAX_RETRY
    重试，4xx 不重试。
    """

    def __init__(self, http):
        self.http = http

    async def fetch_hot_board(self) -> dict:
        resp = await get_with_retry(self.http, config.PP_HOT_BOARD_URL, config.PP_PC_HEADERS)
        return resp.json()

    async def fetch_article_html(self, news_id: str) -> str:
        url = config.PP_ARTICLE_URL.format(news_id=news_id)
        resp = await get_with_retry(self.http, url, config.PP_PC_HEADERS)
        return resp.text
