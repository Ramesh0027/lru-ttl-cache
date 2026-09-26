import unittest

from core import Cache


class Tests(unittest.TestCase):
    def test_lru_and_none(self):
        c = Cache(2)
        c.put("a", None)
        c.put("b", 2)
        self.assertIsNone(c.get("a"))
        c.put("c", 3)
        with self.assertRaises(KeyError):
            c.get("b")
        self.assertEqual(c.stats()["evictions"], 1)

    def test_expiry_precedes_eviction(self):
        now = [0]
        c = Cache(2, lambda: now[0])
        c.put("a", 1, 100)
        c.put("b", 2, 1)
        now[0] = 1
        c.put("c", 3)
        self.assertEqual(c.get("a"), 1)
        self.assertEqual(c.get("b", "missing"), "missing")
        self.assertEqual(c.evictions, 0)

    def test_update_promotes_and_extends(self):
        now = [0]
        c = Cache(1, lambda: now[0])
        c.put("a", 1, 1)
        now[0] = 0.5
        c.put("a", 2, 2)
        now[0] = 1
        self.assertEqual(c.get("a"), 2)
        now[0] = 2.5
        self.assertEqual(len(c), 0)


if __name__ == "__main__":
    unittest.main()
