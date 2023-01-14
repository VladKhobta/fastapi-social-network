from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from ..db import get_session
from ..db import models

from typing import Optional

from .posts import PostsService


class VotesService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    # checking user is not own this post function
    @staticmethod
    def user_is_not_author(
            vote_function: callable
    ):
        def wrapper(self, user_id, post_id):
            posts_service = PostsService(self.session)

            post = posts_service.get(post_id)

            if post.user_id == user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='User cannot vote his own posts'
                )

            return vote_function(self, user_id, post_id)
        return wrapper


    @user_is_not_author
    def like(
            self,
            user_id: int,
            post_id: int,
    ) -> models.Vote:

        vote = self._get(user_id, post_id)

        if not vote:
            vote = models.Vote(
                user_id=user_id,
                post_id=post_id,
                kind='like'
            )
            self.session.add(vote)
            self.session.commit()

            return vote

        if vote.kind == 'like':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Post is already liked by user'
            )

        if vote.kind == 'dislike':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Post is disliked by user'
            )

    @user_is_not_author
    def unlike(
            self,
            user_id: int,
            post_id: int
    ):

        vote = self._get(user_id, post_id)

        if not vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        if vote.kind == 'dislike':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Post is disliked by user'
            )

        self.session.delete(vote)
        self.session.commit()

    @user_is_not_author
    def dislike(
            self,
            user_id: int,
            post_id: int
    ) -> models.Vote:

        vote = self._get(user_id, post_id)

        if not vote:
            vote = models.Vote(
                user_id=user_id,
                post_id=post_id,
                kind='dislike'
            )
            self.session.add(vote)
            self.session.commit()

            return vote

        if vote.kind == 'dislike':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Post is already liked by user'
            )

        if vote.kind == 'like':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Post is liked by user'
            )

    @user_is_not_author
    def remove_dislike(
            self,
            user_id: int,
            post_id: int
    ):

        vote = self._get(user_id, post_id)

        if not vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        if vote.kind == 'like':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Post is liked by user'
            )

        self.session.delete(vote)
        self.session.commit()

    def _get(
            self,
            user_id: int,
            post_id: int,
    ) -> Optional[models.Vote]:
        vote = (
            self.session
            .query(models.Vote)
            .filter(
                models.Vote.user_id == user_id
            )
            .filter(
                models.Vote.post_id == post_id
            )
            .first()
        )

        return vote
