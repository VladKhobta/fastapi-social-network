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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Post is not found'
            )

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
        exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not allowed',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )
        post = self._get(post_id)
        if not post.user_id == user_id:
            raise exception
        for field, value in post_data:
            setattr(post, field, value)
        self.session.commit()
        return post


    def _get_vote(self,
                  post_id: int,
                  user_id: int
    ) -> Optional[models.Vote]:

        vote = (
            self.session
            .query(models.Vote)
            .filter(
                models.Post.id == post_id
            )
            .filter(
                models.User.id == user_id
            )
            .first()
        )

        return vote

    def like(
            self,
            post_id: int,
            user_id: int,
            vote_kind: str
    ) -> Optional[models.Vote]:

        vote = self._get_vote(post_id, user_id)

        if not vote:
            return self._vote_create(post_id, user_id, vote_kind)

        if vote and vote.kind == vote_kind:
            # delete vote record cause it is second click on like button
            pass


    def _vote_create(
            self,
            post_id: int,
            user_id: int,
            vote_kind: str
    ) -> models.Vote:

        vote = models.Vote(
            post_id=post_id,
            user_id=user_id,
            kind=vote_kind
        )
        self.session.add(vote)
        self.session.commit()

        return vote

