from pydantic import BaseModel
from enum import Enum


class VoteKind(str, Enum):
    LIKE = 'like'
    DISLIKE = 'dislike'


class BaseVote(BaseModel):
    kind: VoteKind


class VoteCreate(BaseVote):
    pass


class VoteUpdate(BaseVote):
    pass


class Vote(BaseVote):
    id: int

    class Config:
        orm_mode = True
