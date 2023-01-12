from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship

from .base import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    content = Column(String, index=True)
    date = Column(Date)

    user = relationship('User', backref='posts')
