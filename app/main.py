import os
import sys

from fastapi import FastAPI

# from alembic.env import database_url
from blog import models
from blog.database import engine
from blog.routers import blog, user, authentication, personal_photos, home_photos
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

fastapi_app = FastAPI()
fastapi_app.add_middleware(
    DBSessionMiddleware,
    db_url=os.getenv("DATABASE_URL"),
)
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List the allowed frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

models.Base.metadata.create_all(engine)
# fastapi_app.config["SQLALCHEMY_DATABASE_URI"] = database_url


fastapi_app.include_router(blog.router)
fastapi_app.include_router(user.router)
fastapi_app.include_router(personal_photos.router)
fastapi_app.include_router(authentication.router)
fastapi_app.include_router(home_photos.router)
