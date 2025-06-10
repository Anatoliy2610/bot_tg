from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True


class PostAdd(PostBase):
    pass


class PostUpdate(PostBase):
    new_title: Optional[str] = None
    content: Optional[str] = None


class PostDelete(BaseModel):
    title: str
