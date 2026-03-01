"""文件上传接口模块"""

import logging

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies.auth import get_authorized_headers
from src.schemas.common import Media
from src.schemas.upload import UploadFileRequest
from src.services.upload.info import get_upload_info
from src.services.upload.uploader import upload_file_to_cos

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/v1/upload", response_model=Media)
async def upload_file(
    request: UploadFileRequest,
    headers: dict = Depends(get_authorized_headers),
):
    """文件上传接口

    Args:
        request: 上传请求参数
        headers: 认证请求头

    Returns:
        Media: 上传后的文件信息
    """
    try:
        upload_info = await get_upload_info(request.file.file_name, headers)
        logger.info("Upload info retrieved successfully")
        logger.debug(f"upload_info: {upload_info}")

        file_info = await upload_file_to_cos(request.file, upload_info)
        logger.info("File uploaded successfully")
        logger.debug(f"File uploaded successfully: {file_info}")
        return file_info
    except Exception as e:
        logger.error(f"Error in upload_file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
