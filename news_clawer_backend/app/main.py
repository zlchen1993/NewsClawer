"""FastAPI 应用入口。

启动时建表（create_all）；统一把数据库连接错误转为 503。
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import InterfaceError, OperationalError

from app.db import init_models
from app.routers import crawl, news


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(title="NewsClawer API", version="0.1.0", lifespan=lifespan)


@app.exception_handler(OperationalError)
@app.exception_handler(InterfaceError)
async def _db_unavailable(request: Request, exc: Exception):
    return JSONResponse(status_code=503, content={"detail": "数据库不可用"})


app.include_router(news.router, prefix="/api")
app.include_router(crawl.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
