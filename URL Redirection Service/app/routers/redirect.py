from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from ..redis_config import url_redis, clicks_redis
from ..database import engine
from ..utils import persist_click_count

router = APIRouter(tags=['URL Redirect'])


@router.get('/persist')
async def test():
    await persist_click_count()


@router.get('/{short_url}')
async def redirect_url(short_url: str):
    long_url = await url_redis.get(name=short_url)
    await clicks_redis.incr(name=short_url)
    if not long_url:
        print('URL not in redis')
        async with engine.connect() as db:
            result = await db.execute(text("SELECT long_url FROM urls WHERE short_url = :code"), {"code":short_url})
        result = result.first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Short URL not found')
        long_url = result.long_url
        await url_redis.set(name=short_url, value=long_url)
    else:
        print(f'URL in redis')
    print(long_url)
    return RedirectResponse(url=long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


    