from fastapi import APIRouter

from .auth import router as auth_router
from .posts import router as posts_router
from .votes import router as votes_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(posts_router)
router.include_router(votes_router)
