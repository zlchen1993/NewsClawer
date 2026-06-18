from tools.headers import build_headers, DESKTOP_UA

# 澎湃新闻热榜接口：返回 {"data":{"hotNews":[...]}}
PP_HOT_BOARD_URL = "https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar"
# 文章详情页（HTML，正文嵌在 __NEXT_DATA__ 中）
PP_ARTICLE_URL = "https://www.thepaper.cn/newsDetail_forward_{news_id}"

PP_PC_HEADERS = build_headers(DESKTOP_UA, referer="https://www.thepaper.cn/")
