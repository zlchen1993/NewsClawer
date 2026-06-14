import config


class ToutiaoClient:
    """头条 HTTP 请求封装。接收一个 httpx.AsyncClient（或兼容对象）。"""

    def __init__(self, http):
        self.http = http

    async def fetch_hot_board(self) -> dict:
        resp = await self.http.get(config.TOUTIAO_HOT_BOARD_URL, headers=config.TOUTIAO_PC_HEADERS)
        resp.raise_for_status()
        return resp.json()

    async def fetch_search_html(self, topic_url: str) -> str:
        resp = await self.http.get(topic_url, headers=config.TOUTIAO_PC_HEADERS)
        resp.raise_for_status()
        return resp.text

    async def fetch_article_info(self, gid: str) -> dict:
        url = config.TOUTIAO_ARTICLE_INFO_URL.format(gid=gid)
        resp = await self.http.get(url, headers=config.TOUTIAO_MOBILE_HEADERS)
        resp.raise_for_status()
        return resp.json()
