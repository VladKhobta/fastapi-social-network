from fastapi import APIRouter, Depends, status

from ..schemas import PostCreate, Post, User, PostUpdate
from ..services import get_current_user, PostsService

router = APIRouter(
    prefix='/posts'
)


@router.post('/', response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(
        post_data: PostCreate,
        user: User = Depends(get_current_user),
        posts_service: PostsService = Depends(),
):
    return posts_service.create(
        user.id,
        post_data,
    )


@router.get('/{post_id}', response_model=Post)
def get_post(
        post_id: int,
        posts_service: PostsService = Depends()
):
    return posts_service.get(post_id)


@router.put('/{post_id}', response_model=Post, status_code=status.HTTP_200_OK)
def update_post(
        post_id: int,
        post_data: PostUpdate,
        user: User = Depends(get_current_user),
        posts_service: PostsService = Depends(),
):
    return posts_service.update(
        user.id,
        post_id,
        post_data
    )


