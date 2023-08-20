import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.websockets import WebSocketDisconnect

from blog import models, schemas
from blog.database import engine
from blog.oauth2 import get_current_user
from blog.routers import blog, user, authentication, personal_photos, home_photos

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

websocket_clients_by_group = {}


@fastapi_app.websocket("/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Add the client to the WebSocket group based on the user's ID
    # user_id = current_user.id
    if "trainees" not in websocket_clients_by_group:
        websocket_clients_by_group["trainees"] = []
    websocket_clients_by_group["trainees"].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        websocket_clients_by_group['trainees'].remove(websocket)
