"""上传信息服务模块"""

from typing import Dict

import httpx

UPLOAD_URL = "https://yuanbao.tencent.com/api/resource/genUploadInfo"

DEFAULT_TIMEOUT = 60


class GetUploadInfoError(Exception):
    """获取上传信息异常"""

    pass


async def get_upload_info(file_name: str, headers: Dict[str, str], timeout: int = DEFAULT_TIMEOUT) -> dict:
    """获取上传信息

    Args:
        file_name: 文件名
        headers: 认证请求头
        timeout: 超时时间

    Returns:
        dict: 上传信息

    Raises:
        GetUploadInfoError: 获取上传信息失败时抛出
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                UPLOAD_URL,
                json={"fileName": file_name, "docFrom": "localDoc", "docOpenId": ""},
                headers=headers,
                timeout=timeout,
            )
            response.raise_for_status()
            return response.json()

    except Exception as e:
        raise GetUploadInfoError(e)
