from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from datetime import datetime, timedelta
import requests

from jose import jwt, JWTError
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..settings import settings
from ..db.database import get_session

from ..db import models
from .. import schemas

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth_scheme)) -> schemas.User:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> models.User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = schemas.User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: models.User) -> schemas.Token:
        user_data = schemas.User.from_orm(user)

        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

        return schemas.Token(access_token=token)

    @classmethod
    def validate_email(cls, email: str) -> bool:
        exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Email verification failed',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )

        try:
            req = requests.get(
                f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.email_hunter_api_key}'
            )
            result = req.json()['data']['result']
        except requests.exceptions.RequestException:
            raise exception

        return not result == 'undeliverable'


    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: schemas.UserCreate) -> schemas.Token:
        email_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Email is not valid',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )

        username_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='This username already exists',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )

        if not self.validate_email(user_data.email):
            raise email_exception

        user = models.User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
        )
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            raise username_exception

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> schemas.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )

        user = (
            self.session
            .query(models.User)
            .filter(models.User.username == username)
            .first()
        )

        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)
