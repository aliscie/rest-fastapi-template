from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from .database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # phone = Column(String)
    email = Column(String)
    password = Column(String)

    # exercise = Column(String)
    # diet = Column(String)
    # supplements = Column(String)
    #
    # is_active = Column(Boolean, default=False)
    # is_admin = Column(Boolean, default=False)

    blogs = relationship('Blog', back_populates="creator")
