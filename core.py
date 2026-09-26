import math
import threading
import time
from collections import OrderedDict

MISSING = object()


class Cache:
    def __init__(self, capacity, clock=time.monotonic):
        if type(capacity) is not int or capacity < 1:
            raise ValueError("positive capacity required")
        self.capacity, self.clock = capacity, clock
        self.data = OrderedDict()
        self.lock = threading.RLock()
        self.hits = self.misses = self.evictions = 0

    def _purge(self):
        now = self.clock()
        for key, (_, expires) in list(self.data.items()):
            if expires <= now:
                del self.data[key]

    def put(self, key, value, ttl=60):
        if not math.isfinite(ttl) or ttl <= 0:
            raise ValueError("positive finite TTL required")
        with self.lock:
            self._purge()
            self.data[key] = (value, self.clock() + ttl)
            self.data.move_to_end(key)
            while len(self.data) > self.capacity:
                self.data.popitem(last=False)
                self.evictions += 1

    def get(self, key, default=MISSING):
        with self.lock:
            item = self.data.get(key)
            if item is None or item[1] <= self.clock():
                self.data.pop(key, None)
                self.misses += 1
                if default is MISSING:
                    raise KeyError(key)
                return default
            self.hits += 1
            self.data.move_to_end(key)
            return item[0]

    def __len__(self):
        with self.lock:
            self._purge()
            return len(self.data)

    def clear(self):
        with self.lock:
            self.data.clear()

    def stats(self):
        with self.lock:
            return {
                "hits": self.hits,
                "misses": self.misses,
                "evictions": self.evictions,
                "size": len(self),
            }
