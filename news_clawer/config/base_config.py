# 通用配置
PLATFORM = "toutiao"            # 目标平台
ENABLE_FETCH_CONTENT = True     # 是否抓正文详情
MAX_CONCURRENCY = 5             # 抓正文并发数
REQUEST_TIMEOUT = 15           # 单请求超时（秒）
MAX_RETRY = 3                  # HTTP 重试次数
REQUEST_INTERVAL = 0.0         # 请求间隔（秒，反爬可调）
SAVE_DATA_OPTION = "json"     # 存储方式（首期仅 json）
HOT_LIST_LIMIT = 0            # 热榜抓取条数上限（0=全部）
DATA_DIR = "data"             # 输出根目录

# 浏览器模式相关（仅 BrowserNewsCrawler 平台读取）
HEADLESS = True
LOGIN_TYPE = "qrcode"          # qrcode / cookie
COOKIES = ""
USER_DATA_DIR = "browser_data/%s"


# TX_HOT_BOARD_URL = "https://r.inews.qq.com/gw/event/pc_hot_ranking_list?ids_hash=&offset=0&page_size=50"
