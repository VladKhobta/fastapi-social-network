from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    jwt_secret: str = 'Bq1JZg1LGARjsonIYEP61SFsK4DqACVn2xeztvz1w4w'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600  # token lifetime is one hour

    database_url: str = "sqlite:///./database.sqlite3"

    email_hunter_api_key: str


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
