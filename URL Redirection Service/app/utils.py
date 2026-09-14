from .redis_config import clicks_redis
from sqlalchemy import text
from .database import engine

async def persist_click_count():
    print('PERSISTING CLICK COUNT')
    pipe = clicks_redis.pipeline()
    keys = []
    async for key in clicks_redis.scan_iter(match="*", count=100):
        keys.append(key)
        pipe.getdel(key)

    clicks = await pipe.execute()

    async with engine.begin() as db:
        for url, count in zip(keys,clicks):
            await db.execute(text("""UPDATE urls 
            SET click_count=click_count+:count 
            where short_url=:url"""), 
            {"count":int(count), 
            "url":url})

