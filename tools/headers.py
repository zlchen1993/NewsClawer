"""跨平台共享的 HTTP header 构造器与常用 User-Agent。

新增平台时复用 build_headers(UA, referer=..., 自定义头=...)，
通用头（如 Accept-Language）只在此处维护一份。
"""

# 常用 User-Agent（集中管理，供各平台引用）
DESKTOP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
)

# 所有平台通用的默认头
_COMMON: dict[str, str] = {"Accept-Language": "zh-CN,zh;q=0.9"}


def build_headers(user_agent: str, referer: str | None = None, **extra: str) -> dict:
    """构造统一格式的请求头：通用头 + User-Agent (+ 可选 Referer +额外头)。"""
    headers = {**_COMMON, "User-Agent": user_agent}
    if referer:
        headers["Referer"] = referer
    headers.update(extra)
    return headers
