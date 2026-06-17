# news_clawer_backend

基于 FastAPI 的只读后端，对接爬虫（`news_clawer`）落库到 Postgres 的热点新闻数据。

## 配置

在**仓库根目录**创建 `.env`（参考 `news_clawer_backend/.env.example`）：

```
DATABASE_URL=postgresql+asyncpg://admin:123456@192.168.92.100:15432/newsclawer
```

爬虫与后端共读该 `DATABASE_URL`。

## 启动

依赖已在仓库根 `pyproject.toml` 中（`uv sync` 安装）。从**仓库根目录**运行：

```bash
cd news_clawer_backend
uvicorn app.main:app --reload --port 8000
```

> 应用包 `app` 在导入时会把 `news_clawer/` 注入 `sys.path`，复用爬虫的
> `model` / `store` / `main`（爬虫工厂），无需额外设置 PYTHONPATH。

启动后访问交互式文档：<http://localhost:8000/docs>

## 接口（前缀 `/api`）

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/platforms` | 有数据的平台列表（含最新批次日期、条数） |
| GET | `/api/news?platform=&date=&page=&page_size=&sort=` | 分页热榜；`date` 缺省取最新批次；`sort`=`rank`(默认)/`hot` |
| GET | `/api/news/{id}` | 按代理主键查单条详情 |
| POST | `/api/crawl` `{"platform":"tencent"}` | 后台触发一次爬取并落库，返回 202 |
| GET | `/health` | 健康检查 |

## 让爬虫直接落库

把仓库根爬虫配置 `news_clawer/config/base_config.py` 的 `SAVE_DATA_OPTION` 设为
`"postgres"`，或通过后端 `POST /api/crawl` 触发（该接口强制使用 Postgres 存储）。
