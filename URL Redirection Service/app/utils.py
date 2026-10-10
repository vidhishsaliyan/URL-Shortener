from .redis_config import clicks_redis
from sqlalchemy import text
from .database import engine
from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError

async def persist_click_count():
    print('PERSISTING CLICK COUNT')
    try:
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
    except RedisError as e:
        print('Cannot retrieve click counts from Redis.')

    except SQLAlchemyError as e:
        print('Failed to persist click counts to PostgreSQL.')