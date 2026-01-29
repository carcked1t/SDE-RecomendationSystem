import time
from typing import Any, Optional

# Very simple in-memory cache with TTL for demonstration. Not thread-safe (sufficient for small demo apps).
class SimpleCache:
    def __init__(self):
        self.store = {}  # key -> (expire_ts, value)

    def set(self, key: str, value: Any, ttl: int = 60):
        self.store[key] = (time.time() + ttl, value)

    def get(self, key: str) -> Optional[Any]:
        val = self.store.get(key)
        if not val:
            return None
        expire, v = val
        if time.time() > expire:
            del self.store[key]
            return None
        return v

    def invalidate(self, key: str):
        if key in self.store:
            del self.store[key]

# Shared cache instance
cache = SimpleCache()
