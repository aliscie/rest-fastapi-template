from typing import List, Optional

from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BaseModel):
    title: str = None
    body: str = None

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class User(BaseModel):
    name: str
    email: str
    phone: str
    password: str


class UserUpdate(BaseModel):
    name: str = None
    email: str = None
    phone: str = None
    photo: str = None
    weight: str = None
    height: str = None
    subscription_type: str = None
    expiration: str = None
    exercise: str = None
    diet: str = None
    supplements: str = None

    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class ChangePassword(BaseModel):
    user_id: int = None
    new_password: str


class AllUser(BaseModel):
    name: str
    email: str
    photo: str

    class Config():
        orm_mode = True


class FullUserInfo(BaseModel):
    class Config():
        orm_mode = True


class LoginRes(BaseModel):
    access_token: str
    token_type: str

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    creator: ShowUser

    class Config():
        orm_mode = True


class Login(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class PhotoBase(BaseModel):
    title: str
    content: str
    photo: str


class PhotoCreate(PhotoBase):
    user_id: int
    title: str
    content: str
    photo: str

    class Config:
        orm_mode = True


class GetAllPhotos(PhotoBase):
    user_id: int

    class Config:
        orm_mode = True


class Photo(PhotoBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True


class HomePhotoBase(BaseModel):
    title: str
    content: str
    photo: str
    telegram_link: str


class HomePhotoCreate(HomePhotoBase):
    pass


class HomePhotoUpdate(HomePhotoBase):
    pass


class HomePhoto(HomePhotoBase):
    id: int

    class Config:
        orm_mode = True
