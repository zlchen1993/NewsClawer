from tools.headers import build_headers, DESKTOP_UA

# 腾讯新闻热榜接口：返回 {"ret":0,"idlist":[{"newslist":[...]}]}
TX_HOT_BOARD_URL = "https://i.news.qq.com/gw/event/hot_ranking_list?page_size=50"
# 文章详情页（HTML，正文嵌在 window.DATA 中）
TX_ARTICLE_URL = "https://view.inews.qq.com/a/{news_id}"

TX_PC_HEADERS = build_headers(DESKTOP_UA, referer="https://news.qq.com/")
