from datetime import datetime


def unix_to_str(value) -> str | None:
    """把 unix 秒（int 或数字字符串）转成本地时间字符串；无法解析返回 None。"""
    if value is None:
        return None
    try:
        ts = int(value)
    except (TypeError, ValueError):
        return None
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
