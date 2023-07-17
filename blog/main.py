from fastapi import FastAPI

from app.main import fastapi_app
from . import models
from .database import engine
from .routers import blog, user, authentication


models.Base.metadata.create_all(engine)

fastapi_app.include_router(authentication.router)
fastapi_app.include_router(blog.router)
fastapi_app.include_router(user.router)
