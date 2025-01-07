from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class AdminBase(BaseModel):
    username: str


class AdminCreate(AdminBase):
    password: str


class AdminOut(AdminBase):
    id: int
    username: str

    class Config:
        from_attributes = True
