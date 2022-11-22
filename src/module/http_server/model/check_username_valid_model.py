from pydantic import BaseModel, Field


class CheckUsernameValidModel(BaseModel):
    username: str = Field(..., example='user1')
