from redis.asyncio import Redis
import os
redis_password = os.getenv("REDIS_PASSWORD")

url_redis = Redis(host="url-redis", 
                  port=6379, 
                  password=redis_password,
                  decode_responses=True)

clicks_redis = Redis(host="clicks-redis",
                     port=6379,
                     password=redis_password,
                     decode_responses=True)


