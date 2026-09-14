from redis.asyncio import Redis

url_redis = Redis(host="localhost", 
                  port=6379, 
                  decode_responses=True)

clicks_redis = Redis(host="localhost",
                     port=6380,
                     decode_responses=True)


