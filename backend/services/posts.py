from fastapi import Depends, HTTPException, status

from datetime import datetime

from sqlalchemy.orm import Session

from typing import Optional

from ..schemas.posts import PostCreate, Post, PostUpdate
from ..db.models.posts import Post
from ..db import get_session


class PostsService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, user_id: int, post_data: PostCreate) -> Post:
        now = datetime.utcnow()
        post = Post(**post_data.dict(), created_at=now, user_id=user_id)
        self.session.add(post)
        self.session.commit()
        return post

    def _get(self, post_id: int) -> Optional[Post]:
        post = (
            self.session
            .query(Post)
            .filter(
                Post.id == post_id
            )
            .first()
        )
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return post
