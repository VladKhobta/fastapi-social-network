from fastapi import APIRouter, Depends, status

from ..schemas import PostCreate, Post, User
from ..services import get_current_user, PostsService

router = APIRouter(
    prefix='/posts'
)


@router.post('/', response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(
        post_data: PostCreate,
        user: User = Depends(get_current_user),
        post_service: PostsService = Depends(),
):
    return post_service.create(
        user.id,
        post_data,
    )
