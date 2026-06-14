import json
from datetime import datetime
from pathlib import Path

from model.news import NewsItem
from store.base import AbstractNewsStore


class JsonNewsStore(AbstractNewsStore):
    """按 平台/日期 写 JSON：data/<platform>/<YYYY-MM-DD>.json。

    同文件已存在则按 news_id 去重合并（新数据覆盖旧）。
    """

    def __init__(self, data_dir: str = "data", date_str: str | None = None):
        self.data_dir = data_dir
        self.date_str = date_str or datetime.now().strftime("%Y-%m-%d")

    async def save_batch(self, items: list[NewsItem]) -> None:
        if not items:
            return
        platform = items[0].platform
        out_dir = Path(self.data_dir) / platform
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{self.date_str}.json"

        merged: dict[str, dict] = {}
        if out_file.exists():
            existing = json.loads(out_file.read_text(encoding="utf-8"))
            merged = {d["news_id"]: d for d in existing}
        for item in items:
            merged[item.news_id] = item.model_dump()

        out_file.write_text(
            json.dumps(list(merged.values()), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
