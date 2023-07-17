from typing import Optional

from pydantic import BaseModel

from app.main import fastapi_app


@fastapi_app.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    # only get 10 published blogs
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from the db'}


@fastapi_app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@fastapi_app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {'data': id}


@fastapi_app.get('/blog/{id}/comments')
def comments(id, limit=10):
    # fetch comments of blog with id = id
    return {'data': {'1', '2'}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@fastapi_app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f"Blog is created with title as {blog.title}"}
