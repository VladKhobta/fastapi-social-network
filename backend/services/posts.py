from fastapi import Depends, HTTPException, status

from datetime import datetime

from sqlalchemy.orm import Session

from typing import Optional
from ..db import get_session

from .. import schemas
from ..db import models


class PostsService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, user_id: int, post_data: schemas.PostCreate) -> models.Post:
        now = datetime.utcnow()
        post = models.Post(**post_data.dict(), created_at=now, user_id=user_id)
        self.session.add(post)
        self.session.commit()
        return post


    def _get(self, post_id: int) -> Optional[models.Post]:
        post = (
            self.session
            .query(models.Post)
            .filter(
                models.Post.id == post_id
            )
            .first()
        )
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return post

    def get(self, post_id: int) -> models.Post:
        post = self._get(post_id)
        return post

    def update(
            self,
            user_id: int,
            post_id: int,
            post_data: schemas.PostUpdate
    ) -> models.Post:
        post = self._get(user_id, post_id)
        for field, value in post_data:
            setattr(post, field, value)
        self.session.commit()
        return post


