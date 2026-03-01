"""通用数据模型模块"""

from pydantic import BaseModel


class Media(BaseModel):
    """媒体文件模型"""

    type: str
    docType: str
    url: str
    fileName: str
    size: int
    width: int
    height: int
