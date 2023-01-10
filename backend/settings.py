from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    jwt_secret: str = 'fkl'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600  # token lifetime is one hour

    database_url: str = "sqlite:///./database.sqlite3"


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
