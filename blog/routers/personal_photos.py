from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, schemas, models, oauth2

get_db = database.get_db

router = APIRouter(
    prefix="/photos",
    tags=['Photos']
)


@router.post("/", response_model=schemas.Photo)
def create_photo(
        request: schemas.PhotoCreate,
        # current_user: models.User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)
):
    new_photo = models.BodyPhoto(
        title=request.title,
        content=request.content,
        photo=request.photo,
        creator_id=request.user_id
    )
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return new_photo


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(
        photo_id: int,
        current_user: models.User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)
):
    # current_user = db.query(models.User).filter(models.User.email == email).first()
    photo = db.query(models.BodyPhoto).filter(models.BodyPhoto.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    db.delete(photo)
    db.commit()
    return {'ok': True, 'message': 'Photo deleted successfully'}


@router.get("/", response_model=list[schemas.Photo])
def get_all_photos(
        current_user: models.User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)
):
    # current_user = db.query(models.User).filter(models.User.email == email).first()
    photos = db.query(models.BodyPhoto).all()
    return photos


@router.get("/{user_id}", response_model=list[schemas.Photo])
def get_user_photos(
        user_id: int,
        current_user: models.User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)
):
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Permission denied")

    photos = db.query(models.BodyPhoto).filter(models.BodyPhoto.creator_id == user_id).all()
    return photos
