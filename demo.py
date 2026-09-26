from core import Cache

now = [0]
cache = Cache(2, lambda: now[0])
cache.put("product:1", {"stock": 4}, ttl=10)
print(cache.get("product:1"))
now[0] = 10
print(cache.get("product:1", "expired"))
print(cache.stats())
