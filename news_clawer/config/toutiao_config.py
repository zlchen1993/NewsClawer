from tools.headers import build_headers, DESKTOP_UA, MOBILE_UA

TOUTIAO_HOT_BOARD_URL = "https://www.toutiao.com/hot-event/hot-board/?origin=hot_board"
TOUTIAO_ARTICLE_INFO_URL = "https://m.toutiao.com/i{gid}/info/"

TOUTIAO_PC_HEADERS = build_headers(DESKTOP_UA, referer="https://www.toutiao.com/")
TOUTIAO_MOBILE_HEADERS = build_headers(MOBILE_UA, referer="https://www.toutiao.com/")
