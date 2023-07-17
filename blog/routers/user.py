from fastapi import HTTPException

from fastapi import APIRouter
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from ..hashing import Hash
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.get('/', response_model=list[schemas.ShowUser])
def all(skip: int = 0, db: Session = Depends(get_db), limit: int = 10,
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    # if current_user.is_admin:
    #     ...
    # else:
    #     raise
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.name == request.name).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"duplicate_name",
        )

    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"duplicate_email",
        )

    # if db.query(models.User).filter(models.User.phone == request.phone).first():
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=f"A user with the phone number {request.phone} already exists.",
    #     )

    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password),
                           # phone=request.phone
                           )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)
