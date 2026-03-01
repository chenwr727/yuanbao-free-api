"""应用配置模块"""

import logging
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """应用配置"""

    api_keys: str = Field(
        default="sk-your-api-key-here",
        description="允许的 API Key 列表（逗号分隔）",
    )
    agent_id: str = "naQivTmsDa"
    page_url: str = "https://yuanbao.tencent.com/chat/naQivTmsDa"
    page_timeout: int = 60000
    login_timeout: int = 120000
    qrcode_path: str = "qrcode.png"
    header_timeout: float = 3.0
    header_api_pattern: str = "yuanbao.tencent.com/api"
    upload_host: str = "hunyuan-prod-1258344703.cos.accelerate.myqcloud.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def api_keys_list(self) -> List[str]:
        """获取 API Key 列表"""
        return [key.strip() for key in self.api_keys.split(",") if key.strip()]


settings = Settings()


def validate_api_key(api_key: str) -> bool:
    """验证 API Key 是否有效

    Args:
        api_key: 待验证的 API Key

    Returns:
        bool: 验证是否通过
    """
    return api_key in settings.api_keys_list
