"""playwright 浏览器启动辅助（浏览器模式平台使用）。

首期为骨架：提供启动参数构造与上下文创建辅助，供 BrowserNewsCrawler 调用。
具体平台落地浏览器抓取时再扩展。
"""


def build_launch_options(headless: bool = True) -> dict:
    """构造 playwright 浏览器启动参数。"""
    return {
        "headless": headless,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
    }


async def launch_context(playwright, headless: bool = True):
    """启动 chromium 并返回 (browser, context)。供浏览器模式平台使用。"""
    browser = await playwright.chromium.launch(**build_launch_options(headless))
    context = await browser.new_context()
    return browser, context
