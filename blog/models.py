from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="blogs")


class HomePhoto(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    photo = Column(String)
    telegram_link = Column(String)

    # Specify the primaryjoin parameter
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="home_photos", primaryjoin="HomePhoto.creator_id == User.id")


class BodyPhoto(Base):
    __tablename__ = 'personal_photos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    photo = Column(String)

    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="body_photos")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    # photo in form of list of numbers
    photo = Column(String)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    password = Column(String)
    weight = Column(String)
    height = Column(String)

    exercise = Column(String)
    diet = Column(String)
    supplements = Column(String)
    expiration = Column(String)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    subscription_type = Column(String)

    blogs = relationship('Blog', back_populates="creator")
    body_photos = relationship('BodyPhoto', back_populates="creator")
    home_photos = relationship('HomePhoto', back_populates="creator")
