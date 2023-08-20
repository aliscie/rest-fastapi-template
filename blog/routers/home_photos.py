from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket

from .. import database, schemas, oauth2, models
from ..repository import photo

router = APIRouter(
    prefix="/home_photos",
    tags=['HomePhotos']
)

get_db = database.get_db


@router.get('/')
def get_all_photos(db: Session = Depends(get_db)):
    # reverse the list
    return db.query(models.HomePhoto).all()[::-1]


# @router.post('/')
# def create_photo(
#         request: schemas.HomePhotoCreate,
#         db: Session = Depends(get_db),
#         current_user: schemas.User = Depends(oauth2.get_current_user)
# ):
#     # Ensure that only admins can create photos
#     # if not current_user.is_admin:
#     #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create photos")
#
#     new_photo = photo.create_photo(db, request)
#     return new_photo
#

@router.post('/')
async def create_photo(
        request: schemas.HomePhotoBase,
        db: Session = Depends(get_db),
):
    new_photo = models.HomePhoto(**request.dict())
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    from app.main import websocket_clients_by_group

    connected_clients: List[WebSocket] = []
    for client in websocket_clients_by_group.get('trainees', []):
        await client.send_json({"message": "New photo created!"})

    return new_photo


@router.put('/{photo_id}', response_model=schemas.HomePhoto)
def update_photo(
        photo_id: int,
        request: schemas.HomePhotoUpdate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)
):
    # Ensure that only admins can update photos
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can update photos")

    updated_photo = photo.update_photo(db, photo_id, request)
    if not updated_photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    return updated_photo


@router.delete('/{photo_id}')
def delete_photo(
        photo_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)
):
    # Ensure that only admins can delete photos
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete photos")

    deleted_photo = photo.delete_photo(db, photo_id)
    if not deleted_photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    return deleted_photo
