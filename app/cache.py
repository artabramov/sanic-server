"""Redis cache creator."""

import redis


class CacheCreator:
    def __init__(self, config):
        self.config = config

    async def create_cache(self):
        """Get cache object."""
        return redis.Redis(host=self.config.REDIS_HOST, port=self.config.REDIS_PORT, decode_responses=self.config.REDIS_DECODE)
