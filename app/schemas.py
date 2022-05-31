from pydantic import BaseModel


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
