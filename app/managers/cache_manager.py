"""Cache manager."""

from redis import Redis
from sqlalchemy.ext.serializer import dumps, loads


class CacheManager:
    """Cache Manager provides methods for working with Redis cache."""

    def __init__(self, cache: Redis, log, expire: int = 60) -> None:
        """Init Cache Manager."""
        self.cache = cache
        self.log = log
        self.expire = expire

    async def set(self, obj: object) -> None:
        """Insert SQLAlchemy object in Redis cache."""
        self.cache.set('%s:%s' % (obj.__tablename__, obj.id), dumps(obj), ex=self.expire)
        self.log.debug("Insert SQLAlchemy object into Redis cache, cls=%s, obj=%s" % (
            str(obj.__class__.__name__), str(obj.__dict__)
        ))

    async def get(self, cls: object, obj_id: int) -> object:
        """Select SQLAlchemy object from Redis cache."""
        obj_bytes = self.cache.get('%s:%s' % (cls.__tablename__, obj_id))
        obj = loads(obj_bytes) if obj_bytes else None

        self.log.debug("Select SQLAlchemy object from Redis cache, cls=%s, obj_id=%s, obj=%s" % (
            str(cls.__name__), obj_id, str(obj.__dict__) if obj else None
        ))

        return obj

    async def delete(self, obj: object):
        """Delete SQLAlchemy object from Redis cache."""
        self.cache.delete('%s:%s' % (obj.__tablename__, obj.id))

        self.log.debug("Delete SQLAlchemy object from Redis cache, cls=%s, obj_id=%s" % (
            str(obj.__class__.__name__), str(obj.__dict__)
        ))
