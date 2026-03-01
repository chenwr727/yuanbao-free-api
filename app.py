"""YuanBao API Proxy 主应用"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routers import chat, upload
from src.services.browser import browser_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """应用生命周期事件处理器"""
    logger.info("[Startup] 正在初始化浏览器...")
    try:
        await browser_manager.login()
        logger.info("[Startup] 浏览器初始化完成")
    except Exception as e:
        logger.error(f"[Startup] 浏览器初始化失败: {e}")

    yield

    logger.info("[Shutdown] 正在关闭浏览器...")
    try:
        await browser_manager.close()
        logger.info("[Shutdown] 浏览器已关闭")
    except Exception as e:
        logger.error(f"[Shutdown] 关闭浏览器失败: {e}")


app = FastAPI(title="YuanBao API Proxy", version="1.0.0", lifespan=lifespan)

app.include_router(chat.router)
app.include_router(upload.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
