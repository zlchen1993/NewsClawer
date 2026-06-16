import logging
import sys

_CONFIGURED = False


def get_logger(name: str = "newsclawer") -> logging.Logger:
    """返回带统一格式的 logger（输出到 stderr，UTF-8）。"""
    global _CONFIGURED
    if not _CONFIGURED:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        root = logging.getLogger("newsclawer")
        root.addHandler(handler)
        root.setLevel(logging.INFO)
        _CONFIGURED = True
    return logging.getLogger(name if name.startswith("newsclawer") else f"newsclawer.{name}")
