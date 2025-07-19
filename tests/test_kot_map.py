"""
Unit tests for KotMap class.
"""

import unittest

from kotcollections.kot_map import KotMap


class TestKotMapBasics(unittest.TestCase):
    """Test basic KotMap functionality."""

    def test_init_empty(self):
        """Test creating an empty KotMap."""
        m = KotMap()
        self.assertTrue(m.is_empty())
        self.assertFalse(m.is_not_empty())
        self.assertEqual(m.size, 0)
        self.assertEqual(list(m.keys), [])
        self.assertEqual(list(m.values), [])

    def test_init_from_dict(self):
        """Test creating KotMap from a Python dict."""
        m = KotMap({"a": 1, "b": 2, "c": 3})
        self.assertFalse(m.is_empty())
        self.assertTrue(m.is_not_empty())
        self.assertEqual(m.size, 3)
        self.assertTrue(m.contains_key("a"))
        self.assertTrue(m.contains_key("b"))
        self.assertTrue(m.contains_key("c"))
        self.assertEqual(m.get("a"), 1)
        self.assertEqual(m.get("b"), 2)
        self.assertEqual(m.get("c"), 3)

    def test_init_from_list_of_tuples(self):
        """Test creating KotMap from a list of tuples."""
        m = KotMap([("a", 1), ("b", 2), ("c", 3)])
        self.assertEqual(m.size, 3)
        self.assertEqual(m.get("a"), 1)
        self.assertEqual(m.get("b"), 2)
        self.assertEqual(m.get("c"), 3)

    def test_init_from_iterator(self):
        """Test creating KotMap from an iterator."""
        m = KotMap((str(i), i) for i in range(5))
        self.assertEqual(m.size, 5)
        for i in range(5):
            self.assertTrue(m.contains_key(str(i)))
            self.assertEqual(m.get(str(i)), i)

    def test_type_safety_keys(self):
        """Test that all keys must be of the same type."""
        m = KotMap({1: "a", 2: "b", 3: "c"})
        with self.assertRaises(TypeError):
            KotMap({1: "a", "2": "b", 3: "c"})

    def test_type_safety_values(self):
        """Test that all values must be of the same type."""
        m = KotMap({"a": 1, "b": 2, "c": 3})
        with self.assertRaises(TypeError):
            KotMap({"a": 1, "b": "2", "c": 3})

    def test_nested_kot_maps(self):
        """Test that KotMap can contain other KotMap instances."""
        inner1 = KotMap({"x": 1, "y": 2})
        inner2 = KotMap({"x": 3, "y": 4})
        outer = KotMap({"first": inner1, "second": inner2})
        
        self.assertEqual(outer.size, 2)
        self.assertEqual(outer.get("first"), inner1)
        self.assertEqual(outer.get("second"), inner2)
        self.assertEqual(outer.get("first").get("x"), 1)

    def test_none_keys_and_values(self):
        """Test that None can be used as keys and values."""
        m1 = KotMap({None: 1, "a": 2})
        self.assertTrue(m1.contains_key(None))
        self.assertEqual(m1.get(None), 1)
        
        m2 = KotMap({"a": None, "b": None})
        self.assertTrue(m2.contains_value(None))
        self.assertIsNone(m2.get("a"))


class TestKotMapAccess(unittest.TestCase):
    """Test KotMap access operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMap({"a": 1, "b": 2, "c": 3, "d": 4})

    def test_get(self):
        """Test get method."""
        self.assertEqual(self.map.get("a"), 1)
        self.assertEqual(self.map.get("b"), 2)
        self.assertIsNone(self.map.get("z"))

    def test_get_or_default(self):
        """Test get_or_default method."""
        self.assertEqual(self.map.get_or_default("a", 99), 1)
        self.assertEqual(self.map.get_or_default("z", 99), 99)

    def test_get_or_else(self):
        """Test get_or_else method."""
        self.assertEqual(self.map.get_or_else("a", lambda: 99), 1)
        self.assertEqual(self.map.get_or_else("z", lambda: 99), 99)
        
        # Test that lambda is only called when needed
        counter = 0
        def increment():
            nonlocal counter
            counter += 1
            return 99
        
        self.map.get_or_else("a", increment)
        self.assertEqual(counter, 0)  # Should not be called
        
        self.map.get_or_else("z", increment)
        self.assertEqual(counter, 1)  # Should be called

    def test_get_or_null_and_none(self):
        """Test get_or_null and get_or_none methods."""
        self.assertEqual(self.map.get_or_null("a"), 1)
        self.assertIsNone(self.map.get_or_null("z"))
        
        # Test alias
        self.assertEqual(self.map.get_or_none("a"), 1)
        self.assertIsNone(self.map.get_or_none("z"))

    def test_contains_key(self):
        """Test contains_key method."""
        self.assertTrue(self.map.contains_key("a"))
        self.assertTrue(self.map.contains_key("b"))
        self.assertFalse(self.map.contains_key("z"))

    def test_contains_value(self):
        """Test contains_value method."""
        self.assertTrue(self.map.contains_value(1))
        self.assertTrue(self.map.contains_value(2))
        self.assertFalse(self.map.contains_value(99))

    def test_keys_values_entries(self):
        """Test keys, values, and entries properties."""
        keys = self.map.keys
        self.assertEqual(len(keys), 4)
        self.assertIn("a", keys)
        self.assertIn("b", keys)
        self.assertIn("c", keys)
        self.assertIn("d", keys)
        
        values = self.map.values
        self.assertEqual(len(values), 4)
        self.assertIn(1, values)
        self.assertIn(2, values)
        self.assertIn(3, values)
        self.assertIn(4, values)
        
        entries = self.map.entries
        self.assertEqual(len(entries), 4)
        self.assertIn(("a", 1), entries)
        self.assertIn(("b", 2), entries)
        self.assertIn(("c", 3), entries)
        self.assertIn(("d", 4), entries)

    def test_getitem(self):
        """Test [] operator."""
        self.assertEqual(self.map["a"], 1)
        self.assertEqual(self.map["b"], 2)
        with self.assertRaises(KeyError):
            _ = self.map["z"]


class TestKotMapChecking(unittest.TestCase):
    """Test KotMap checking operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMap({"a": 1, "b": 2, "c": 3, "d": 4})

    def test_all(self):
        """Test all method."""
        self.assertTrue(self.map.all(lambda k, v: v > 0))
        self.assertTrue(self.map.all(lambda k, v: len(k) == 1))
        self.assertFalse(self.map.all(lambda k, v: v > 2))

    def test_any(self):
        """Test any method."""
        self.assertTrue(self.map.any(lambda k, v: v > 3))
        self.assertTrue(self.map.any(lambda k, v: k == "a"))
        self.assertFalse(self.map.any(lambda k, v: v > 10))

    def test_none(self):
        """Test none method."""
        self.assertTrue(self.map.none(lambda k, v: v > 10))
        self.assertFalse(self.map.none(lambda k, v: v > 2))

    def test_count(self):
        """Test count method."""
        self.assertEqual(self.map.count(), 4)
        self.assertEqual(self.map.count(lambda k, v: v > 2), 2)
        self.assertEqual(self.map.count(lambda k, v: v > 10), 0)


class TestKotMapFiltering(unittest.TestCase):
    """Test KotMap filtering operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMap({"a": 1, "b": 2, "c": 3, "d": 4})

    def test_filter(self):
        """Test filter method."""
        filtered = self.map.filter(lambda k, v: v > 2)
        self.assertEqual(filtered.size, 2)
        self.assertTrue(filtered.contains_key("c"))
        self.assertTrue(filtered.contains_key("d"))
        self.assertFalse(filtered.contains_key("a"))
        self.assertFalse(filtered.contains_key("b"))

    def test_filter_not(self):
        """Test filter_not method."""
        filtered = self.map.filter_not(lambda k, v: v > 2)
        self.assertEqual(filtered.size, 2)
        self.assertTrue(filtered.contains_key("a"))
        self.assertTrue(filtered.contains_key("b"))
        self.assertFalse(filtered.contains_key("c"))
        self.assertFalse(filtered.contains_key("d"))

    def test_filter_keys(self):
        """Test filter_keys method."""
        filtered = self.map.filter_keys(lambda k: k in ["a", "c"])
        self.assertEqual(filtered.size, 2)
        self.assertTrue(filtered.contains_key("a"))
        self.assertTrue(filtered.contains_key("c"))

    def test_filter_values(self):
        """Test filter_values method."""
        filtered = self.map.filter_values(lambda v: v % 2 == 0)
        self.assertEqual(filtered.size, 2)
        self.assertTrue(filtered.contains_key("b"))
        self.assertTrue(filtered.contains_key("d"))

    def test_filter_not_null_and_none(self):
        """Test filter_not_null and filter_not_none methods."""
        m = KotMap({"a": 1, "b": None, "c": 3, "d": None})
        filtered = m.filter_not_null()
        self.assertEqual(filtered.size, 2)
        self.assertTrue(filtered.contains_key("a"))
        self.assertTrue(filtered.contains_key("c"))
        
        # Test alias
        filtered2 = m.filter_not_none()
        self.assertEqual(filtered2.size, 2)
        self.assertEqual(filtered, filtered2)


class TestKotMapTransformation(unittest.TestCase):
    """Test KotMap transformation operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMap({"a": 1, "b": 2, "c": 3})

    def test_map(self):
        """Test map method."""
        result = self.map.map(lambda k, v: f"{k}:{v}")
        self.assertEqual(len(result), 3)
        self.assertIn("a:1", result)
        self.assertIn("b:2", result)
        self.assertIn("c:3", result)

    def test_map_keys(self):
        """Test map_keys method."""
        result = self.map.map_keys(lambda k, v: k.upper())
        self.assertEqual(result.size, 3)
        self.assertTrue(result.contains_key("A"))
        self.assertTrue(result.contains_key("B"))
        self.assertTrue(result.contains_key("C"))
        self.assertEqual(result.get("A"), 1)
        self.assertEqual(result.get("B"), 2)
        self.assertEqual(result.get("C"), 3)

    def test_map_values(self):
        """Test map_values method."""
        result = self.map.map_values(lambda k, v: v * 10)
        self.assertEqual(result.size, 3)
        self.assertEqual(result.get("a"), 10)
        self.assertEqual(result.get("b"), 20)
        self.assertEqual(result.get("c"), 30)

    def test_map_not_null_and_none(self):
        """Test map_not_null and map_not_none methods."""
        result = self.map.map_not_null(lambda k, v: v if v > 1 else None)
        self.assertEqual(len(result), 2)
        self.assertIn(2, result)
        self.assertIn(3, result)
        self.assertNotIn(1, result)
        
        # Test alias
        result2 = self.map.map_not_none(lambda k, v: v if v > 1 else None)
        self.assertEqual(result, result2)

    def test_flat_map(self):
        """Test flat_map method."""
        result = self.map.flat_map(lambda k, v: [k, str(v)])
        self.assertEqual(len(result), 6)
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertIn("1", result)
        self.assertIn("2", result)
        self.assertIn("3", result)


class TestKotMapAggregation(unittest.TestCase):
    """Test KotMap aggregation operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMap({"a": 1, "b": 2, "c": 3, "d": 4})

    def test_max_by(self):
        """Test max_by method."""
        result = self.map.max_by(lambda k, v: v)
        self.assertEqual(result, ("d", 4))
        
        result2 = self.map.max_by(lambda k, v: k)
        self.assertEqual(result2, ("d", 4))

    def test_max_by_or_null_and_none(self):
        """Test max_by_or_null and max_by_or_none methods."""
        result = self.map.max_by_or_null(lambda k, v: v)
        self.assertEqual(result, ("d", 4))
        
        empty = KotMap()
        self.assertIsNone(empty.max_by_or_null(lambda k, v: v))
        
        # Test alias
        result2 = self.map.max_by_or_none(lambda k, v: v)
        self.assertEqual(result, result2)

    def test_min_by(self):
        """Test min_by method."""
        result = self.map.min_by(lambda k, v: v)
        self.assertEqual(result, ("a", 1))
        
        result2 = self.map.min_by(lambda k, v: k)
        self.assertEqual(result2, ("a", 1))

    def test_min_by_or_null_and_none(self):
        """Test min_by_or_null and min_by_or_none methods."""
        result = self.map.min_by_or_null(lambda k, v: v)
        self.assertEqual(result, ("a", 1))
        
        empty = KotMap()
        self.assertIsNone(empty.min_by_or_null(lambda k, v: v))
        
        # Test alias
        result2 = self.map.min_by_or_none(lambda k, v: v)
        self.assertEqual(result, result2)


class TestKotMapConversion(unittest.TestCase):
    """Test KotMap conversion operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMap({"a": 1, "b": 2, "c": 3})

    def test_to_list(self):
        """Test to_list method."""
        result = self.map.to_list()
        self.assertEqual(len(result), 3)
        self.assertIn(("a", 1), result)
        self.assertIn(("b", 2), result)
        self.assertIn(("c", 3), result)

    def test_to_dict(self):
        """Test to_dict method."""
        result = self.map.to_dict()
        self.assertEqual(result, {"a": 1, "b": 2, "c": 3})
        self.assertIsInstance(result, dict)
        # Ensure it's a copy
        result["d"] = 4
        self.assertFalse(self.map.contains_key("d"))

    def test_join_to_string(self):
        """Test join_to_string method."""
        result = self.map.join_to_string()
        # Default format
        parts = result.split(", ")
        self.assertEqual(len(parts), 3)
        
        # Custom separator
        result = self.map.join_to_string(separator=" | ")
        parts = result.split(" | ")
        self.assertEqual(len(parts), 3)
        
        # With prefix and postfix
        result = self.map.join_to_string(prefix="[", postfix="]")
        self.assertTrue(result.startswith("["))
        self.assertTrue(result.endswith("]"))
        
        # With limit
        result = self.map.join_to_string(limit=2)
        self.assertIn("...", result)
        
        # With custom transform
        result = self.map.join_to_string(transform=lambda k, v: f"{k}->{v}")
        self.assertIn("a->1", result)


class TestKotMapActions(unittest.TestCase):
    """Test KotMap action operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMap({"a": 1, "b": 2, "c": 3})

    def test_for_each(self):
        """Test for_each method."""
        result = []
        self.map.for_each(lambda k, v: result.append((k, v)))
        self.assertEqual(len(result), 3)
        self.assertIn(("a", 1), result)
        self.assertIn(("b", 2), result)
        self.assertIn(("c", 3), result)

    def test_on_each(self):
        """Test on_each method."""
        result = []
        returned = self.map.on_each(lambda k, v: result.append((k, v)))
        self.assertEqual(returned, self.map)  # Should return self
        self.assertEqual(len(result), 3)


class TestKotMapSpecialMethods(unittest.TestCase):
    """Test KotMap special methods."""

    def test_len(self):
        """Test __len__ method."""
        m = KotMap({"a": 1, "b": 2, "c": 3})
        self.assertEqual(len(m), 3)
        
        empty = KotMap()
        self.assertEqual(len(empty), 0)

    def test_contains(self):
        """Test __contains__ method."""
        m = KotMap({"a": 1, "b": 2, "c": 3})
        self.assertIn("a", m)
        self.assertIn("b", m)
        self.assertNotIn("z", m)

    def test_iter(self):
        """Test __iter__ method."""
        m = KotMap({"a": 1, "b": 2, "c": 3})
        keys = list(m)
        self.assertEqual(len(keys), 3)
        self.assertIn("a", keys)
        self.assertIn("b", keys)
        self.assertIn("c", keys)

    def test_repr(self):
        """Test __repr__ method."""
        m = KotMap({"a": 1, "b": 2})
        repr_str = repr(m)
        self.assertTrue(repr_str.startswith("KotMap("))
        self.assertTrue(repr_str.endswith(")"))

    def test_eq(self):
        """Test __eq__ method."""
        m1 = KotMap({"a": 1, "b": 2})
        m2 = KotMap({"a": 1, "b": 2})
        m3 = KotMap({"a": 1, "b": 3})
        m4 = KotMap({"a": 1})
        
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
        self.assertNotEqual(m1, m4)
        self.assertNotEqual(m1, {"a": 1, "b": 2})  # Not equal to dict

    def test_hash(self):
        """Test __hash__ method."""
        m1 = KotMap({"a": 1, "b": 2})
        m2 = KotMap({"a": 1, "b": 2})
        
        # Equal maps should have equal hashes
        self.assertEqual(hash(m1), hash(m2))
        
        # Can be used in sets
        s = {m1}
        self.assertIn(m1, s)
        self.assertIn(m2, s)  # Equal map should be in set
        
        # Hash should be cached
        h1 = hash(m1)
        h2 = hash(m1)
        self.assertEqual(h1, h2)


class TestKotMapEdgeCases(unittest.TestCase):
    """Test KotMap edge cases."""

    def test_empty_map_operations(self):
        """Test operations on empty map."""
        m = KotMap()
        
        self.assertTrue(m.is_empty())
        self.assertIsNone(m.get("any"))
        self.assertEqual(m.get_or_default("any", 99), 99)
        self.assertFalse(m.contains_key("any"))
        self.assertFalse(m.contains_value(1))
        
        self.assertTrue(m.all(lambda k, v: True))
        self.assertFalse(m.any(lambda k, v: True))
        self.assertTrue(m.none(lambda k, v: True))
        self.assertEqual(m.count(), 0)
        
        self.assertEqual(m.filter(lambda k, v: True).size, 0)
        self.assertEqual(len(m.map(lambda k, v: v)), 0)
        
        self.assertIsNone(m.max_by_or_null(lambda k, v: v))
        self.assertIsNone(m.min_by_or_null(lambda k, v: v))

    def test_single_element_map(self):
        """Test operations on single element map."""
        m = KotMap({"only": 42})
        
        self.assertEqual(m.size, 1)
        self.assertEqual(m.get("only"), 42)
        self.assertTrue(m.all(lambda k, v: v == 42))
        self.assertTrue(m.any(lambda k, v: v == 42))
        self.assertFalse(m.none(lambda k, v: v == 42))
        
        self.assertEqual(m.max_by(lambda k, v: v), ("only", 42))
        self.assertEqual(m.min_by(lambda k, v: v), ("only", 42))


if __name__ == '__main__':
    unittest.main()