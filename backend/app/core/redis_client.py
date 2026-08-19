import json
import time
import logging
from typing import Optional, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class MemoryCache:
    """In-memory fallback cache when Redis server is offline."""
    def __init__(self):
        self._store = {}
        self._expiry = {}

    def get(self, key: str) -> Optional[str]:
        if key in self._expiry and self._expiry[key] < time.time():
            self.delete(key)
            return None
        return self._store.get(key)

    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        self._store[key] = value
        if ex:
            self._expiry[key] = time.time() + ex
        elif key in self._expiry:
            del self._expiry[key]
        return True

    def setex(self, key: str, time_sec: int, value: str) -> bool:
        return self.set(key, value, ex=time_sec)

    def delete(self, *keys: str) -> int:
        count = 0
        for k in keys:
            if k in self._store:
                del self._store[k]
                count += 1
            if k in self._expiry:
                del self._expiry[k]
        return count

    def ping(self) -> bool:
        return True

    def flushall(self):
        self._store.clear()
        self._expiry.clear()


class CacheClient:
    def __init__(self):
        self.client = None
        self.is_redis = False
        try:
            import redis
            r = redis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=1)
            r.ping()
            self.client = r
            self.is_redis = True
            logger.info("Connected to Redis instance successfully.")
        except Exception:
            logger.warning("Redis unavailable. Using high-performance in-memory cache fallback.")
            self.client = MemoryCache()
            self.is_redis = False

    def get_json(self, key: str) -> Optional[Any]:
        try:
            val = self.client.get(key)
            return json.loads(val) if val else None
        except Exception:
            return None

    def set_json(self, key: str, value: Any, ex: Optional[int] = 300) -> bool:
        try:
            val = json.dumps(value)
            if self.is_redis and ex:
                return bool(self.client.setex(key, ex, val))
            else:
                return bool(self.client.set(key, val, ex=ex))
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    def delete(self, *keys: str) -> int:
        try:
            return self.client.delete(*keys)
        except Exception:
            return 0

    def ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except Exception:
            return False


cache = CacheClient()
