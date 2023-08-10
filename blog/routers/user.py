from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .. import database, schemas, models, oauth2
from ..hashing import Hash
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.User).filter(models.User.id == user_id).first()

    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(obj)
    db.commit()

    return {'ok': True, 'message': 'User successfully deleted.'}


@router.get('/')
def all(
        skip: int = 0,
        db: Session = Depends(get_db),
        limit: int = 10,
        current_user: schemas.User = Depends(oauth2.get_current_user)
):
    # if current_user.is_admin:
    #     ...
    # else:
    #     raise
    # users = db.query(models.User).offset(skip).limit(limit).all()
    users = db.query(models.User).all()
    return users


def cehck_dupilcatoin(db, request):
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

    if db.query(models.User).filter(models.User.phone == request.phone).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"duplicate_phone",
        )


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    admins_number = db.query(models.User).filter(models.User.is_admin == True).count()
    is_admin = False
    if admins_number < 3:
        is_admin = True

    cehck_dupilcatoin(db, request)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
        phone=request.phone,
        is_admin=is_admin,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}')
def get_user(id: int, db: Session = Depends(get_db)):
    user_data = user.show(id, db).__dict__
    # Remove the password key from the dictionary
    user_data.pop("password", None)
    return user_data


@router.put("/{id}")
def update_user(id: int, request: schemas.UserUpdate, db: Session = Depends(get_db)):
    cehck_dupilcatoin(db, request)
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # print(request)

    for key, value in request.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return db.query(models.User).filter(models.User.id == id).first()


@router.post('/change-password', response_model=schemas.ShowUser)
def change_password(
        request: schemas.ChangePassword,
        current_user: models.User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)
):
    # current_user = db.query(models.User).filter(models.User.email == email).first()
    if (request.user_id is None) or (current_user.is_admin is False):
        target_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    else:
        target_user = db.query(models.User).filter(models.User.id == request.user_id).first()

    target_user.password = Hash.bcrypt(request.new_password)

    # db.add(target_user)
    db.commit()
    db.refresh(target_user)
    return target_user
