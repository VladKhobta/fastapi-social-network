from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, MetaData, Date
from sqlalchemy.orm import relationship

from .base import Base


class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey('users.id'), index=True, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), index=True, primary_key=True)
    kind = Column(String)
