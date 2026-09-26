# Lru Ttl Cache

![Project cover](docs/cover.svg)

A bounded thread-safe LRU cache with per-entry expiration and hit/miss statistics.

An independent engineering lab by Ramesh Yenduri. Examples use synthetic data.

## Run

Python 3.12+; standard library only, no package installation required.

```sh
python demo.py
python -m unittest -v
```

## Design and behavior

`Cache.put(key,value,ttl)` inserts with a monotonic expiration time; `get()` promotes successful reads. Expired entries are removed before choosing an LRU eviction, so stale values never displace live ones unnecessarily. Cached `None` remains distinguishable from a missing key through `KeyError` or a caller-supplied default. Expiration tests require no sleeps.

## Read the code

- `core.py` — implementation and public API.
- `demo.py` — deterministic, runnable usage example.
- `test_core.py` — behavior and failure-path tests.
- `.github/workflows/ci.yml` — runs the suite on Python 3.12 and 3.13.

## Scope and tradeoffs

In-memory and process-local. Expiry cleanup scans the bounded cache on put/len, trading simplicity for O(n) work. It has no background sweeper, serialization, distributed invalidation or cache-stampede prevention. Statistics are cumulative and do not reset on clear.
