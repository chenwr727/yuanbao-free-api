"""上传相关数据模型模块"""

from pydantic import BaseModel


class File(BaseModel):
    """文件模型"""

    file_name: str
    file_data: str
    file_type: str


class UploadFileRequest(BaseModel):
    """上传文件请求模型"""

    file: File
