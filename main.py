from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/blog')
def blog(limit = 10, publish:bool= True, sort:Optional[str] = None):
    if publish:
        return {'data': f'{limit} publish blogs from db'}
    else:
        return {'data': f'{limit} blogs from db'}


@app.get("/get")
def root():
    return "hello world"



@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]



@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f"Blog is created with title as {request.title}"}