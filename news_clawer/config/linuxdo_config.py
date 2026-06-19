# LinuxDo（Discourse 论坛）需走浏览器模式：站点有 Cloudflare 人机校验，
# 普通 HTTP 请求会被 403 拦截，故用 BrowserNewsCrawler 先过校验再取 JSON。
LINUXDO_HOME_URL = "https://linux.do/"
# 当日热门话题（Discourse top 接口）
LINUXDO_TOP_PATH = "/top.json?period=daily"
# 等待 Cloudflare 校验通过的轮询次数（每次约 1.5s）
LINUXDO_CF_WAIT_TRIES = 20
