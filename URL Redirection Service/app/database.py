from sqlalchemy.ext.asyncio import create_async_engine
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL)
