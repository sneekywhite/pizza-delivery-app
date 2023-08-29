from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(Blog):
    title: str
    body: str

    class Config:
        orm_mode = True
    


class User(BaseModel):
    name: str
    email: str
    password: str


class Show_user(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True



