import redis

r = redis.StrictRedis(host='redis', port=6379, db=0)

# import aioredis

# class RedisClient:
#     def __init__(self):
#         self.redis = None

#     async def connect(self):
#         self.redis = await aioredis.from_url("redis://redis:6379/0")

#     async def close(self):
#         if self.redis:
#             await self.redis.close()

#     async def get(self, key):
#         if self.redis:
#             return await self.redis.get(key)

#     async def set(self, key, value):
#         if self.redis:
#             await self.redis.set(key, value)

#     async def delete(self, key):
#         if self.redis:
#             await self.redis.delete(key)

# r = RedisClient()


