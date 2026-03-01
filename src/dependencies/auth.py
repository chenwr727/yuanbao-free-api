"""认证依赖模块"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.config import validate_api_key
from src.utils.common import generate_headers

bearer_scheme = HTTPBearer(auto_error=False)


async def get_authorized_headers(
    authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """获取授权的请求头

    Args:
        authorization: Bearer token 认证信息

    Returns:
        dict: 包含认证信息的请求头

    Raises:
        HTTPException: 认证失败时抛出
    """
    if not authorization or not authorization.credentials:
        raise HTTPException(status_code=401, detail="need token")

    token = authorization.credentials

    if not validate_api_key(token):
        raise HTTPException(status_code=403, detail="invalid api_key")

    headers = await generate_headers()

    return headers
