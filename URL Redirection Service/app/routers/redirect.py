from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from ..config import settings
from ..redis_config import url_redis
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL)

router = APIRouter(tags=['URL Redirect'])

@router.get('/{short_url}')
async def redirect_url(short_url: str):
    long_url = await url_redis.get(name=f'url:{short_url}')
    if not long_url:
        print('URL not in redis')
        async with engine.connect() as db:
            result = await db.execute(text("SELECT long_url FROM urls WHERE short_url = :code"), {"code":short_url})
        result = result.first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Short URL not found')
        long_url = result.long_url
        await url_redis.set(name=f'url:{short_url}', value=long_url)
    else:
        print(f'URL in redis')
    print(long_url)
    return RedirectResponse(url=long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)