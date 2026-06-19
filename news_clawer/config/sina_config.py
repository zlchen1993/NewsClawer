from tools.headers import build_headers, MOBILE_UA

# 新浪新闻热榜接口：返回 {"data":{"hotList":[...]}}
SINA_HOT_LIST_URL = (
    "https://newsapp.sina.cn/api/hotlist?newsId=HB-1-snhs%2Ftop_news_list-all"
)

SINA_MOBILE_HEADERS = build_headers(MOBILE_UA, referer="https://news.sina.cn/")
