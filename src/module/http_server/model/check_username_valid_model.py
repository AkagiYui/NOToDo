from pydantic import BaseModel, Field


class CheckUsernameValidModel(BaseModel):
    """检查用户名是否合法 数据模型"""

    username: str = Field(..., example='user1')
