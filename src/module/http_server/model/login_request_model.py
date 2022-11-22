from pydantic import BaseModel, Field


class LoginRequestModel(BaseModel):
    """登录 数据模型"""

    username: str = Field(..., example='admin')
    password: str = Field(..., example='adminadmin')
