from pydantic import BaseModel, Field


class RegisterRequestModel(BaseModel):
    username: str = Field(..., example='admin')
    password: str = Field(..., example='mypwd')
    nickname: str = Field(..., example='这是昵称')
    email: str = Field(..., example='这是邮箱')
