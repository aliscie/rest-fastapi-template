from sqlalchemy.orm import Session
from .. import models, schemas


# def get_all_photos(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(models.HomePhoto).offset(skip).limit(limit).all()


def create_photo(db: Session, photo: schemas.HomePhotoBase):
    new_photo = models.HomePhoto(**photo.dict())
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return new_photo


def update_photo(db: Session, photo_id: int, photo: schemas.HomePhotoUpdate):
    existing_photo = db.query(models.HomePhoto).filter(models.HomePhoto.id == photo_id).first()
    if existing_photo:
        for attr, value in photo.dict(exclude_unset=True).items():
            setattr(existing_photo, attr, value)
        db.commit()
        db.refresh(existing_photo)
        return existing_photo
    return None


def delete_photo(db: Session, photo_id: int):
    existing_photo = db.query(models.HomePhoto).filter(models.HomePhoto.id == photo_id).first()
    if existing_photo:
        db.delete(existing_photo)
        db.commit()
        return existing_photo
    return None
