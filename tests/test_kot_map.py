"""
Unit tests for KotMap class.
"""

import unittest

from kotcollections.kot_map import KotMap
from kotcollections.kot_mutable_map import KotMutableMap
from kotcollections.kot_list import KotList
from kotcollections.kot_mutable_list import KotMutableList


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
        from kotcollections import KotList
        result = self.map.map(lambda k, v: f"{k}:{v}")
        self.assertIsInstance(result, KotList)
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
        from kotcollections import KotList
        result = self.map.map_not_null(lambda k, v: v if v > 1 else None)
        self.assertIsInstance(result, KotList)
        self.assertEqual(len(result), 2)
        self.assertIn(2, result)
        self.assertIn(3, result)
        self.assertNotIn(1, result)
        
        # Test alias
        result2 = self.map.map_not_none(lambda k, v: v if v > 1 else None)
        self.assertEqual(result, result2)

    def test_flat_map(self):
        """Test flat_map method."""
        from kotcollections import KotList
        result = self.map.flat_map(lambda k, v: [k, str(v)])
        self.assertIsInstance(result, KotList)
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


class TestKotMapNewMethods(unittest.TestCase):
    """Test newly added KotMap methods for Kotlin compatibility."""

    def test_get_value(self):
        """Test getValue() method that throws exception for missing keys."""
        m = KotMap({"a": 1, "b": 2, "c": 3})
        
        # Test getting existing values
        self.assertEqual(m.get_value("a"), 1)
        self.assertEqual(m.get_value("b"), 2)
        self.assertEqual(m.get_value("c"), 3)
        
        # Test exception for missing key
        with self.assertRaises(KeyError) as context:
            m.get_value("missing")
        self.assertIn("missing", str(context.exception))

    def test_plus_method(self):
        """Test plus() method and + operator."""
        m1 = KotMap({"a": 1, "b": 2})
        m2 = KotMap({"c": 3, "d": 4})
        
        # Test plus with another KotMap
        m3 = m1.plus(m2)
        self.assertEqual(m3.size, 4)
        self.assertEqual(m3.get("a"), 1)
        self.assertEqual(m3.get("b"), 2)
        self.assertEqual(m3.get("c"), 3)
        self.assertEqual(m3.get("d"), 4)
        
        # Test that original maps are unchanged
        self.assertEqual(m1.size, 2)
        self.assertEqual(m2.size, 2)
        
        # Test plus with dict
        m4 = m1.plus({"e": 5, "f": 6})
        self.assertEqual(m4.size, 4)
        self.assertEqual(m4.get("e"), 5)
        self.assertEqual(m4.get("f"), 6)
        
        # Test plus with tuple (single pair)
        m5 = m1.plus(("g", 7))
        self.assertEqual(m5.size, 3)
        self.assertEqual(m5.get("g"), 7)
        
        # Test overwriting existing keys
        m6 = m1.plus({"a": 10, "new": 20})
        self.assertEqual(m6.get("a"), 10)  # Should be overwritten
        self.assertEqual(m6.get("new"), 20)
        
        # Test + operator
        m7 = m1 + m2
        self.assertEqual(m7.size, 4)
        m8 = m1 + ("h", 8)
        self.assertEqual(m8.get("h"), 8)

    def test_minus_method(self):
        """Test minus() method and - operator."""
        m = KotMap({"a": 1, "b": 2, "c": 3, "d": 4})
        
        # Test minus with single key
        m1 = m.minus("a")
        self.assertEqual(m1.size, 3)
        self.assertFalse(m1.contains_key("a"))
        self.assertTrue(m1.contains_key("b"))
        
        # Test minus with list of keys
        m2 = m.minus(["a", "c"])
        self.assertEqual(m2.size, 2)
        self.assertFalse(m2.contains_key("a"))
        self.assertFalse(m2.contains_key("c"))
        self.assertTrue(m2.contains_key("b"))
        self.assertTrue(m2.contains_key("d"))
        
        # Test minus with set of keys
        m3 = m.minus({"b", "d"})
        self.assertEqual(m3.size, 2)
        self.assertTrue(m3.contains_key("a"))
        self.assertTrue(m3.contains_key("c"))
        
        # Test minus with non-existent key
        m4 = m.minus("non-existent")
        self.assertEqual(m4.size, 4)  # Should remain unchanged
        
        # Test that original map is unchanged
        self.assertEqual(m.size, 4)
        
        # Test - operator
        m5 = m - "a"
        self.assertEqual(m5.size, 3)
        m6 = m - ["a", "b"]
        self.assertEqual(m6.size, 2)

    def test_with_default(self):
        """Test withDefault() method and KotMapWithDefault class."""
        from kotcollections import KotMapWithDefault
        
        m = KotMap({"a": 1, "b": 2})
        
        # Create a map with default value function
        m_with_default = m.with_default(lambda k: len(k))
        
        # Test that it's an instance of KotMapWithDefault
        self.assertIsInstance(m_with_default, KotMapWithDefault)
        
        # Test getting existing values
        self.assertEqual(m_with_default.get("a"), 1)
        self.assertEqual(m_with_default.get("b"), 2)
        
        # Test getting non-existent values (should use default function)
        self.assertEqual(m_with_default.get("xxx"), 3)  # len("xxx") = 3
        self.assertEqual(m_with_default.get("hello"), 5)  # len("hello") = 5
        
        # Test with [] operator
        self.assertEqual(m_with_default["a"], 1)
        self.assertEqual(m_with_default["missing"], 7)  # len("missing") = 7
        
        # Test getValue() - should not throw exception
        self.assertEqual(m_with_default.get_value("new"), 3)  # len("new") = 3
        
        # Test that original map is unchanged
        self.assertIsNone(m.get("xxx"))
        
        # Test withDefault with numeric default
        m_numeric = KotMap({"x": 10, "y": 20})
        m_with_numeric_default = m_numeric.with_default(lambda k: 0)
        self.assertEqual(m_with_numeric_default.get("z"), 0)
        
        # Test withDefault preserves type safety
        # (The default function should return the correct type)
        m_str = KotMap({"key1": "value1"})
        m_str_default = m_str.with_default(lambda k: f"default_{k}")
        self.assertEqual(m_str_default.get("key2"), "default_key2")
        
        # Test get_or_default - should always use the map's default function
        self.assertEqual(m_str_default.get_or_default("key3", "ignored"), "default_key3")
        self.assertEqual(m_str_default.get_or_default("key1", "ignored"), "value1")
        
        # Test get_or_else - should always use the map's default function, not the provided one
        self.assertEqual(m_str_default.get_or_else("key4", lambda: "should_not_be_used"), "default_key4")
        self.assertEqual(m_str_default.get_or_else("key1", lambda: "should_not_be_used"), "value1")


class TestKotMapInheritanceTypeChecking(unittest.TestCase):
    """Test type checking with inheritance relationships for KotMap."""
    
    def setUp(self):
        """Set up test classes with inheritance."""
        class Animal:
            def __init__(self, name):
                self.name = name
        
        class Dog(Animal):
            pass
        
        class Cat(Animal):
            pass
        
        self.Animal = Animal
        self.Dog = Dog
        self.Cat = Cat
    
    def test_parent_type_accepts_subclass_values(self):
        """Test that parent type map accepts subclass values."""
        # Create map with parent type value
        animal_map = KotMap({"animal1": self.Animal("Generic")})
        mutable_map = animal_map.to_kot_mutable_map()
        
        # Should work - adding Dog to Animal map
        mutable_map.put("dog1", self.Dog("Buddy"))
        self.assertEqual(mutable_map.size, 2)
        self.assertIsInstance(mutable_map.get("animal1"), self.Animal)
        self.assertIsInstance(mutable_map.get("dog1"), self.Dog)
        
        # Should also work - adding Cat to Animal map
        mutable_map.put("cat1", self.Cat("Whiskers"))
        self.assertEqual(mutable_map.size, 3)
        self.assertIsInstance(mutable_map.get("cat1"), self.Cat)
    
    def test_subclass_type_rejects_parent_values(self):
        """Test that subclass type map rejects parent class values."""
        # Create map with subclass type value
        dog_map = KotMap({"dog1": self.Dog("Buddy")})
        mutable_map = dog_map.to_kot_mutable_map()
        
        # Should fail - adding Animal to Dog map
        with self.assertRaises(TypeError) as cm:
            mutable_map.put("animal1", self.Animal("Generic"))
        self.assertIn("Cannot add element of type 'Animal' to KotMap value", str(cm.exception))
    
    def test_different_subclasses_cannot_mix(self):
        """Test that different subclasses cannot be mixed."""
        # Create map with Dog type value
        dog_map = KotMap({"dog1": self.Dog("Buddy")})
        mutable_map = dog_map.to_kot_mutable_map()
        
        # Should fail - adding Cat to Dog map
        with self.assertRaises(TypeError) as cm:
            mutable_map.put("cat1", self.Cat("Whiskers"))
        self.assertIn("Cannot add element of type 'Cat' to KotMap value", str(cm.exception))
    
    def test_initialization_with_mixed_types(self):
        """Test initialization with mixed parent/subclass types."""
        # Should work when parent comes first
        mixed_map = KotMap({
            "animal1": self.Animal("Generic"),
            "dog1": self.Dog("Buddy")
        })
        self.assertEqual(mixed_map.size, 2)
        self.assertIsInstance(mixed_map.get("animal1"), self.Animal)
        self.assertIsInstance(mixed_map.get("dog1"), self.Dog)
        
        # Should fail when subclass comes first
        with self.assertRaises(TypeError) as cm:
            KotMap({
                "dog1": self.Dog("Buddy"),
                "animal1": self.Animal("Generic")
            })
        # Note: dict ordering is preserved in Python 3.7+
        self.assertIn("Cannot add element of type 'Animal' to KotMap value", str(cm.exception))
    
    def test_key_type_inheritance(self):
        """Test that key type checking also works with inheritance."""
        # Using custom classes as keys (they need to be hashable)
        class HashableAnimal:
            def __init__(self, name):
                self.name = name
            def __hash__(self):
                return hash(self.name)
            def __eq__(self, other):
                return isinstance(other, HashableAnimal) and self.name == other.name
        
        class HashableDog(HashableAnimal):
            pass
        
        # Parent type keys accept subclass keys
        animal_key_map = KotMap({HashableAnimal("Generic"): "value1"})
        mutable_map = animal_key_map.to_kot_mutable_map()
        mutable_map.put(HashableDog("Buddy"), "value2")
        self.assertEqual(mutable_map.size, 2)
        
        # Subclass type keys reject parent keys
        dog_key_map = KotMap({HashableDog("Buddy"): "value1"})
        mutable_map2 = dog_key_map.to_kot_mutable_map()
        with self.assertRaises(TypeError) as cm:
            mutable_map2.put(HashableAnimal("Generic"), "value2")
        self.assertIn("Cannot add element of type 'HashableAnimal' to KotMap key", str(cm.exception))


class TestKotMapTypeSpecification(unittest.TestCase):
    def test_class_getitem_syntax(self):
        """Test __class_getitem__ for type specification"""
        # Define test classes with inheritance
        class Animal:
            def __init__(self, name):
                self.name = name
        
        class Dog(Animal):
            pass
        
        class Cat(Animal):
            pass
        
        # Test creating typed KotMap with parent types
        animals_by_name = KotMap[str, Animal]()
        self.assertEqual(len(animals_by_name), 0)
        
        # Convert to mutable and add different subclass instances
        mutable_animals = animals_by_name.to_kot_mutable_map()
        mutable_animals.put("Buddy", Dog("Buddy"))
        mutable_animals.put("Whiskers", Cat("Whiskers"))
        self.assertEqual(len(mutable_animals), 2)
        
        # Test with initial elements
        animals2 = KotMap[str, Animal]([("Max", Dog("Max")), ("Luna", Cat("Luna"))])
        self.assertEqual(len(animals2), 2)
        self.assertIsInstance(animals2.get("Max"), Dog)
        self.assertIsInstance(animals2.get("Luna"), Cat)
    
    def test_of_type_method(self):
        """Test of_type class method for type specification"""
        # Define test classes with inheritance
        class Animal:
            def __init__(self, name):
                self.name = name
        
        class Dog(Animal):
            pass
        
        class Cat(Animal):
            pass
        
        # Test creating empty typed KotMap
        animals_by_name = KotMap.of_type(str, Animal)
        self.assertEqual(len(animals_by_name), 0)
        
        # Convert to mutable and add different subclass instances
        mutable_animals = animals_by_name.to_kot_mutable_map()
        mutable_animals.put("Buddy", Dog("Buddy"))
        mutable_animals.put("Whiskers", Cat("Whiskers"))
        self.assertEqual(len(mutable_animals), 2)
        
        # Test with initial elements (list of tuples)
        animals2 = KotMap.of_type(str, Animal, [("Max", Dog("Max")), ("Luna", Cat("Luna"))])
        self.assertEqual(len(animals2), 2)
        self.assertIsInstance(animals2.get("Max"), Dog)
        self.assertIsInstance(animals2.get("Luna"), Cat)
        
        # Test with initial elements (dict)
        animals3 = KotMap.of_type(str, Animal, {"Rex": Dog("Rex"), "Mittens": Cat("Mittens")})
        self.assertEqual(len(animals3), 2)
        self.assertIsInstance(animals3.get("Rex"), Dog)
        self.assertIsInstance(animals3.get("Mittens"), Cat)
        
        # Test type checking is enforced
        class NotAnimal:
            pass
        
        mutable_animals2 = animals2.to_kot_mutable_map()
        with self.assertRaises(TypeError):
            mutable_animals2.put("Invalid", NotAnimal())
    
    def test_type_preservation_in_conversions(self):
        """Test that type information is preserved during conversions"""
        # Define test classes with inheritance
        class Animal:
            def __init__(self, name):
                self.name = name
        
        class Dog(Animal):
            pass
        
        # Test KotMap type preservation
        animal_map = KotMap.of_type(str, Animal, {"dog1": Dog("Buddy")})
        self.assertEqual(animal_map._key_type, str)
        self.assertEqual(animal_map._value_type, Animal)
        
        # Test to_kot_map preserves types
        copied = animal_map.to_kot_map()
        self.assertEqual(copied._key_type, str)
        self.assertEqual(copied._value_type, Animal)
        
        # Test to_kot_mutable_map preserves types
        mutable = animal_map.to_kot_mutable_map()
        self.assertEqual(mutable._key_type, str)
        self.assertEqual(mutable._value_type, Animal)
        # Verify we can still add correct types
        mutable.put("dog2", Dog("Max"))
        self.assertEqual(len(mutable), 2)
    
    def test_kot_list_value_type_with_class_getitem(self):
        """Test KotMap with KotList[T] as value type using __class_getitem__ syntax"""
        # Define test classes
        class Holiday:
            def __init__(self, name):
                self.name = name
        
        import datetime
        
        # Create a map with KotList[Holiday] as value type using __class_getitem__ syntax
        cache = KotMutableMap[datetime.date, KotList[Holiday]]()
        
        # Create a mutable list with Holiday type
        holidays = KotMutableList[Holiday]()
        holidays.add(Holiday("New Year"))
        holidays.add(Holiday("Christmas"))
        
        # Convert to immutable KotList
        immutable_holidays = holidays.to_kot_list()
        
        # This should work without TypeError
        today = datetime.date.today()
        cache.put(today, immutable_holidays)
        
        # Verify the value was stored correctly
        retrieved = cache.get(today)
        self.assertEqual(len(retrieved), 2)
        self.assertEqual(retrieved[0].name, "New Year")
        self.assertEqual(retrieved[1].name, "Christmas")
    
    def test_kot_list_key_type_with_class_getitem(self):
        """Test KotMap with KotList[T] as key type using __class_getitem__ syntax"""
        # Define test classes
        class Tag:
            def __init__(self, name):
                self.name = name
                
        # Create a map with KotList[Tag] as key type using __class_getitem__ syntax
        tag_map = KotMutableMap[KotList[Tag], str]()
        
        # Create a mutable list with Tag type
        tags1 = KotMutableList[Tag]()
        tags1.add(Tag("python"))
        tags1.add(Tag("kotlin"))
        
        # Convert to immutable KotList
        immutable_tags1 = tags1.to_kot_list()
        
        # This should work without TypeError
        tag_map.put(immutable_tags1, "Programming languages")
        
        # Create another tag list
        tags2 = KotMutableList[Tag]()
        tags2.add(Tag("java"))
        
        # Convert to immutable KotList
        immutable_tags2 = tags2.to_kot_list()
        tag_map.put(immutable_tags2, "JVM language")
        
        # Verify the values were stored correctly
        self.assertEqual(tag_map.size, 2)
        self.assertEqual(tag_map.get(immutable_tags1), "Programming languages")
        self.assertEqual(tag_map.get(immutable_tags2), "JVM language")


if __name__ == '__main__':
    unittest.main()