from fastapi import APIRouter, Depends, status

from ..schemas import Vote, User
from ..services import get_current_user, VotesService

router = APIRouter(
    prefix='/votes'
)


@router.post('/{post_id}/like')
def like(
        post_id: int,
        user: User = Depends(get_current_user),
        votes_service: VotesService = Depends()
):
    return votes_service.like(user.id, post_id)


@router.post('/{post_id}/unlike')
def unlike(
        post_id: int,
        user: User = Depends(get_current_user),
        votes_service: VotesService = Depends()
):
    return votes_service.unlike(user.id, post_id)


@router.post('/{post_id}/dislike')
def dislike(
        post_id: int,
        user: User = Depends(get_current_user),
        votes_service: VotesService = Depends()
):
    return votes_service.dislike(user.id, post_id)


@router.post('/{post_id}/remove_dislike')
def remove_dislike(
        post_id: int,
        user: User = Depends(get_current_user),
        votes_service: VotesService = Depends()
):
    return votes_service.remove_dislike(user.id, post_id)
