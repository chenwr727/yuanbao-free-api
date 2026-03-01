"""文件上传到 COS 服务模块"""

import base64
from typing import Dict

import httpx

from src.config import settings
from src.schemas.upload import File
from src.utils.upload import generate_headers, get_file_info

DEFAULT_TIMEOUT = 60


class UploadFileToCosError(Exception):
    """上传文件到 COS 异常"""

    pass


async def upload_file_to_cos(
    file: File,
    upload_info: Dict,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict:
    """上传文件到腾讯云 COS

    Args:
        file: 文件信息
        upload_info: 上传信息
        timeout: 超时时间

    Returns:
        Dict: 文件信息

    Raises:
        UploadFileToCosError: 上传失败时抛出
    """
    try:
        url = f"https://{settings.upload_host}{upload_info['location']}"

        file_data_bytes = base64.b64decode(file.file_data)
        content_length = len(file_data_bytes)
        headers = generate_headers(file.file_type, content_length, settings.upload_host, upload_info)

        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=headers, content=file_data_bytes, timeout=timeout)
            if response.status_code != 200:
                raise Exception(f"Request failed. Status code: {response.status_code}, Response: {response.text}")

            return get_file_info(
                file.file_type,
                file.file_name,
                content_length,
                upload_info["resourceUrl"],
                response.text,
            )

    except Exception as e:
        raise UploadFileToCosError(e)
