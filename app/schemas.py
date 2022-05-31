from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_model = True


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
