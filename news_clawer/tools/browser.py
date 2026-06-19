"""playwright 浏览器启动辅助（浏览器模式平台使用）。

提供启动参数构造与上下文创建辅助，供 BrowserNewsCrawler 调用。
默认带桌面 UA / 中文 locale，便于通过 Cloudflare 等人机校验。
"""

from tools.headers import DESKTOP_UA


def build_launch_options(headless: bool = True) -> dict:
    """构造 playwright 浏览器启动参数。"""
    return {
        "headless": headless,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
    }


async def launch_context(
    playwright, headless: bool = True, user_agent: str = DESKTOP_UA, locale: str = "zh-CN"
):
    """启动 chromium 并返回 (browser, context)。供浏览器模式平台使用。

    默认注入桌面 UA 与中文 locale（避免 HeadlessChrome UA 被风控直接拦截）。
    """
    browser = await playwright.chromium.launch(**build_launch_options(headless))
    context = await browser.new_context(user_agent=user_agent, locale=locale)
    return browser, context
