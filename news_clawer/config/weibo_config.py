from tools.headers import build_headers, DESKTOP_UA

# 微博热搜接口：返回 {"data":{"realtime":[...]}}（无需登录）
WB_HOT_SEARCH_URL = "https://weibo.com/ajax/side/hotSearch"

WB_PC_HEADERS = build_headers(DESKTOP_UA, referer="https://weibo.com/")
