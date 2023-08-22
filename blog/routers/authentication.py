from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, token
from ..hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.name == request.name).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    user.force_logout = False
    db.commit()
    db.refresh(user)

    access_token = token.create_access_token(data={"sub": user.email})
    user_data = user.__dict__
    # Remove the password key from the dictionary
    user_data.pop("password", None)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data
    }
