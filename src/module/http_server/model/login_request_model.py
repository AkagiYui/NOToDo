from pydantic import BaseModel, Field


class LoginRequestModel(BaseModel):
    username: str = Field(..., example='admin')
    password: str = Field(..., example='adminadmin')
