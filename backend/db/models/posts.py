from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, MetaData, Date
from sqlalchemy.orm import relationship

from .base import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime)

    user = relationship('User', backref='posts')
