from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):  # Display User Info as response including Password
    id: int
    email: EmailStr
    password: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserIdOut(BaseModel):  # Display User Info as response without Password
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
