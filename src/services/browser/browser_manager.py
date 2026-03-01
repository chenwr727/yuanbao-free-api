"""浏览器管理器模块"""

import asyncio
import logging
from typing import Dict, Optional

from playwright.async_api import Browser, Page, async_playwright

from src.config import settings
from src.utils.qr_utils import print_qr_to_terminal

logger = logging.getLogger(__name__)


class BrowserManager:
    """浏览器管理器 - 单例模式"""

    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.browser: Optional[Browser] = None
            self.page: Optional[Page] = None
            self.playwright = None
            self._route_handler = None
            self._is_logged_in = False
            self._initialized = True

    async def ensure_browser(self):
        """确保浏览器已初始化"""
        async with self._lock:
            if self.browser is None or self.page is None:
                await self._init_browser()

    async def _init_browser(self):
        """初始化浏览器"""
        if self.playwright is None:
            self.playwright = await async_playwright().start()

        if self.browser is None:
            self.browser = await self.playwright.chromium.launch(headless=True)

        if self.page is None:
            self.page = await self.browser.new_page()
            await self._load_page()

    async def _load_page(self):
        """预加载页面"""
        logger.info("[Browser] 预加载 Yuanbao 页面...")
        try:
            await self.page.goto(settings.page_url, timeout=settings.page_timeout)
            await self.page.wait_for_timeout(3000)
            logger.info("[Browser] 页面加载完成")
        except Exception as e:
            logger.error(f"[Browser] 页面加载失败: {e}")
            raise

    async def login(self) -> Dict:
        """执行登录流程，返回二维码信息

        Returns:
            Dict: 登录结果字典
        """
        await self.ensure_browser()

        try:
            login_button = self.page.get_by_role("img").first
            await login_button.wait_for(state="visible")
            await login_button.click()

            iframe_frame = self.page.frame_locator("iframe")
            qrcode_locator = iframe_frame.get_by_role("img")
            await qrcode_locator.wait_for(state="visible", timeout=10000)

            await qrcode_locator.screenshot(path=settings.qrcode_path)
            logger.info(f"[Browser] 二维码已保存至 {settings.qrcode_path}")

            print_qr_to_terminal(settings.qrcode_path)

            logger.info("[Browser] 等待扫码完成...")
            try:
                await login_button.wait_for(state="detached", timeout=settings.login_timeout)
                logger.info("[Browser] 扫码成功，按钮已消失")
                self._is_logged_in = True
                return {
                    "success": True,
                    "message": "登录成功",
                    "qrcode_path": settings.qrcode_path,
                }
            except TimeoutError:
                logger.warning("[Browser] 扫码超时或未检测到登录成功")
                return {
                    "success": False,
                    "message": "扫码超时",
                    "qrcode_path": settings.qrcode_path,
                }
        except Exception as e:
            logger.error(f"[Browser] 登录失败: {e}")
            return {
                "success": False,
                "message": f"登录失败: {str(e)}",
            }

    async def get_headers(self) -> Optional[Dict]:
        """获取请求头

        Returns:
            Optional[Dict]: 请求头字典，失败返回 None
        """
        await self.ensure_browser()
        captured_headers = {}

        async def handle_route(route, request):
            nonlocal captured_headers
            url = request.url
            headers = request.headers

            if settings.header_api_pattern in url:
                if "x-uskey" in headers and not captured_headers.get("x-uskey"):
                    captured_headers = headers
                    logger.info(f"[Browser] 捕获到请求头 from {url}")

            await route.continue_()

        if self._route_handler:
            try:
                self.page.remove_route("**/*")
            except Exception:
                pass

        await self.page.route("**/*", handle_route)
        self._route_handler = handle_route

        try:
            reload_task = asyncio.create_task(self.page.reload(timeout=10000))

            start_time = asyncio.get_event_loop().time()

            while (asyncio.get_event_loop().time() - start_time) < settings.header_timeout:
                if captured_headers.get("x-uskey"):
                    break
                await asyncio.sleep(0.05)

            if captured_headers.get("x-uskey"):
                reload_task.cancel()
                try:
                    await reload_task
                except asyncio.CancelledError:
                    pass

        except Exception as e:
            logger.error(f"[Browser] 获取请求头失败: {e}")
        finally:
            if self._route_handler:
                try:
                    self.page.remove_route("**/*")
                    self._route_handler = None
                except Exception:
                    pass

        return captured_headers if captured_headers.get("x-uskey") else None

    async def get_cookies(self) -> Dict[str, str]:
        """获取 Cookie

        Returns:
            Dict[str, str]: Cookie 字典
        """
        await self.ensure_browser()

        if not self.page:
            return {}

        cookies = await self.page.context.cookies()
        return {c["name"]: c["value"] for c in cookies}

    async def close(self):
        """关闭浏览器"""
        async with self._lock:
            tasks = []
            if self.page:
                tasks.append(self.page.close())
                self.page = None
            if self.browser:
                tasks.append(self.browser.close())
                self.browser = None
            if self.playwright:
                tasks.append(self.playwright.stop())
                self.playwright = None
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)


# 全局单例
browser_manager = BrowserManager()
