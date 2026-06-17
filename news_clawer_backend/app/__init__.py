"""后端应用包。

导入时把爬虫源码根 news_clawer/ 注入 sys.path，使本包可直接
`import model / store / main`（复用爬虫的模型、共享 DB 层与爬虫工厂）。
必须在包初始化阶段完成，先于 app.* 子模块导入爬虫代码。
"""

import sys
from pathlib import Path

_CRAWLER_ROOT = Path(__file__).resolve().parents[2] / "news_clawer"
if _CRAWLER_ROOT.is_dir() and str(_CRAWLER_ROOT) not in sys.path:
    sys.path.insert(0, str(_CRAWLER_ROOT))
