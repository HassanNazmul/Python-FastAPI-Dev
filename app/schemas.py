from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True


# class Post(PostBase):
#     id: int

#     class Config:
#         orm_mode = True


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True


# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserIDOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
