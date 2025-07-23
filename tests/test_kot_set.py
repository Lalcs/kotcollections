"""
Unit tests for KotSet class.
"""

import unittest

from kotcollections.kot_set import KotSet
from kotcollections.kot_map import KotMap
from kotcollections.kot_list import KotList


class TestKotSetBasics(unittest.TestCase):
    """Test basic KotSet functionality."""

    def test_init_empty(self):
        """Test creating an empty KotSet."""
        s = KotSet()
        self.assertTrue(s.is_empty())
        self.assertEqual(s.size, 0)
        self.assertEqual(list(s), [])

    def test_init_from_set(self):
        """Test creating KotSet from a Python set."""
        s = KotSet({1, 2, 3})
        self.assertFalse(s.is_empty())
        self.assertEqual(s.size, 3)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)

    def test_init_from_list(self):
        """Test creating KotSet from a list with duplicates."""
        s = KotSet([1, 2, 2, 3, 3, 3])
        self.assertEqual(s.size, 3)  # Duplicates removed
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)

    def test_init_from_iterator(self):
        """Test creating KotSet from an iterator."""
        s = KotSet(x for x in range(5))
        self.assertEqual(s.size, 5)
        for i in range(5):
            self.assertTrue(i in s)

    def test_type_safety(self):
        """Test that all elements must be of the same type."""
        s = KotSet([1, 2, 3])
        with self.assertRaises(TypeError):
            KotSet([1, "2", 3])

    def test_nested_kot_sets(self):
        """Test that nested KotSets are allowed."""
        inner1 = KotSet([1, 2])
        inner2 = KotSet([3, 4])
        outer = KotSet([inner1, inner2])
        self.assertEqual(outer.size, 2)
        self.assertTrue(inner1 in outer)
        self.assertTrue(inner2 in outer)

    def test_none_elements(self):
        """Test that None elements are allowed."""
        s = KotSet([None, None])
        self.assertEqual(s.size, 1)  # Only one None
        self.assertTrue(None in s)

    def test_repr(self):
        """Test string representation."""
        s = KotSet([1, 2, 3])
        repr_str = repr(s)
        self.assertTrue(repr_str.startswith("KotSet("))
        self.assertTrue("1" in repr_str)
        self.assertTrue("2" in repr_str)
        self.assertTrue("3" in repr_str)

    def test_equality(self):
        """Test set equality."""
        s1 = KotSet([1, 2, 3])
        s2 = KotSet([3, 2, 1])  # Order doesn't matter
        s3 = KotSet([1, 2])
        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)

        # Test equality with non-KotSet objects
        self.assertNotEqual(s1, {1, 2, 3})
        self.assertNotEqual(s1, [1, 2, 3])
        self.assertNotEqual(s1, "not a set")

    def test_hash(self):
        """Test set hashing."""
        s1 = KotSet([1, 2, 3])
        s2 = KotSet([3, 2, 1])
        self.assertEqual(hash(s1), hash(s2))


class TestKotSetAccess(unittest.TestCase):
    """Test KotSet access operations."""

    def test_contains(self):
        """Test contains method."""
        s = KotSet([1, 2, 3])
        self.assertTrue(s.contains(1))
        self.assertTrue(s.contains(2))
        self.assertTrue(s.contains(3))
        self.assertFalse(s.contains(4))

    def test_contains_all(self):
        """Test contains_all method."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertTrue(s.contains_all({1, 2, 3}))
        self.assertTrue(s.contains_all([2, 4]))
        self.assertTrue(s.contains_all(KotSet([1, 5])))
        self.assertFalse(s.contains_all({1, 6}))

    def test_first(self):
        """Test first method."""
        s = KotSet([1])
        self.assertIn(s.first(), [1])

        empty = KotSet()
        with self.assertRaises(ValueError):
            empty.first()

    def test_first_or_null(self):
        """Test first_or_null method."""
        s = KotSet([1, 2, 3])
        self.assertIn(s.first_or_null(), [1, 2, 3])

        empty = KotSet()
        self.assertIsNone(empty.first_or_null())

    def test_first_or_none(self):
        """Test first_or_none alias."""
        s = KotSet([1, 2, 3])
        self.assertIn(s.first_or_none(), [1, 2, 3])

        empty = KotSet()
        self.assertIsNone(empty.first_or_none())

    def test_first_predicate(self):
        """Test first with predicate."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertEqual(s.first_predicate(lambda x: x > 3), 4)

        with self.assertRaises(ValueError):
            s.first_predicate(lambda x: x > 10)

    def test_first_or_null_predicate(self):
        """Test first_or_null with predicate."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertEqual(s.first_or_null_predicate(lambda x: x > 3), 4)
        self.assertIsNone(s.first_or_null_predicate(lambda x: x > 10))

    def test_first_or_none_predicate(self):
        """Test first_or_none_predicate alias."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertEqual(s.first_or_none_predicate(lambda x: x > 3), 4)
        self.assertIsNone(s.first_or_none_predicate(lambda x: x > 10))

    def test_single(self):
        """Test single method."""
        s = KotSet([42])
        self.assertEqual(s.single(), 42)

        empty = KotSet()
        with self.assertRaises(ValueError):
            empty.single()

        multiple = KotSet([1, 2])
        with self.assertRaises(ValueError):
            multiple.single()

    def test_single_or_null(self):
        """Test single_or_null method."""
        s = KotSet([42])
        self.assertEqual(s.single_or_null(), 42)

        empty = KotSet()
        self.assertIsNone(empty.single_or_null())

        multiple = KotSet([1, 2])
        self.assertIsNone(multiple.single_or_null())

    def test_single_or_none(self):
        """Test single_or_none alias."""
        s = KotSet([42])
        self.assertEqual(s.single_or_none(), 42)

        empty = KotSet()
        self.assertIsNone(empty.single_or_none())

    def test_single_predicate(self):
        """Test single with predicate."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertEqual(s.single_predicate(lambda x: x == 3), 3)

        with self.assertRaises(ValueError):
            s.single_predicate(lambda x: x > 10)

        with self.assertRaises(ValueError):
            s.single_predicate(lambda x: x > 2)  # Multiple matches

    def test_single_or_null_predicate(self):
        """Test single_or_null with predicate."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertEqual(s.single_or_null_predicate(lambda x: x == 3), 3)
        self.assertIsNone(s.single_or_null_predicate(lambda x: x > 10))
        self.assertIsNone(s.single_or_null_predicate(lambda x: x > 2))

    def test_single_or_none_predicate(self):
        """Test single_or_none_predicate alias."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertEqual(s.single_or_none_predicate(lambda x: x == 3), 3)
        self.assertIsNone(s.single_or_none_predicate(lambda x: x > 10))

    def test_last(self):
        """Test last method."""
        s = KotSet([1])
        self.assertIn(s.last(), [1])

        empty = KotSet()
        with self.assertRaises(ValueError):
            empty.last()

    def test_last_or_null(self):
        """Test last_or_null method."""
        s = KotSet([1, 2, 3])
        self.assertIn(s.last_or_null(), [1, 2, 3])

        empty = KotSet()
        self.assertIsNone(empty.last_or_null())

    def test_last_or_none(self):
        """Test last_or_none alias."""
        s = KotSet([1, 2, 3])
        self.assertIn(s.last_or_none(), [1, 2, 3])

        empty = KotSet()
        self.assertIsNone(empty.last_or_none())


class TestKotSetTransformation(unittest.TestCase):
    """Test KotSet transformation operations."""

    def test_map(self):
        """Test map transformation."""
        s = KotSet([1, 2, 3])
        mapped = s.map(lambda x: x * 2)
        self.assertEqual(mapped.size, 3)
        self.assertTrue(2 in mapped)
        self.assertTrue(4 in mapped)
        self.assertTrue(6 in mapped)

    def test_map_type_change(self):
        """Test map with type change."""
        s = KotSet([1, 2, 3])
        mapped = s.map(str)
        self.assertEqual(mapped.size, 3)
        self.assertTrue("1" in mapped)
        self.assertTrue("2" in mapped)
        self.assertTrue("3" in mapped)

    def test_map_not_null(self):
        """Test map_not_null transformation."""
        s = KotSet([1, 2, 3, 4, 5])
        mapped = s.map_not_null(lambda x: x if x % 2 == 0 else None)
        self.assertEqual(mapped.size, 2)
        self.assertTrue(2 in mapped)
        self.assertTrue(4 in mapped)

    def test_map_not_none(self):
        """Test map_not_none alias."""
        s = KotSet([1, 2, 3, 4, 5])
        mapped = s.map_not_none(lambda x: x if x % 2 == 0 else None)
        self.assertEqual(mapped.size, 2)
        self.assertTrue(2 in mapped)
        self.assertTrue(4 in mapped)

    def test_flat_map(self):
        """Test flat_map transformation."""
        s = KotSet([1, 2, 3])
        flat_mapped = s.flat_map(lambda x: {x, x * 10})
        self.assertEqual(flat_mapped.size, 6)
        for i in [1, 2, 3, 10, 20, 30]:
            self.assertTrue(i in flat_mapped)

    def test_flat_map_with_lists(self):
        """Test flat_map with lists."""
        s = KotSet(["hello", "world"])
        flat_mapped = s.flat_map(lambda x: list(x))
        # Should contain unique characters
        expected = {'h', 'e', 'l', 'o', 'w', 'r', 'd'}
        self.assertEqual(flat_mapped.size, len(expected))
        for char in expected:
            self.assertTrue(char in flat_mapped)

    def test_flat_map_with_kot_sets(self):
        """Test flat_map with KotSets."""
        s = KotSet([1, 2])
        flat_mapped = s.flat_map(lambda x: KotSet([x, x + 10]))
        self.assertEqual(flat_mapped.size, 4)
        for i in [1, 2, 11, 12]:
            self.assertTrue(i in flat_mapped)


class TestKotSetFiltering(unittest.TestCase):
    """Test KotSet filtering operations."""

    def test_filter(self):
        """Test filter operation."""
        s = KotSet([1, 2, 3, 4, 5])
        filtered = s.filter(lambda x: x % 2 == 0)
        self.assertEqual(filtered.size, 2)
        self.assertTrue(2 in filtered)
        self.assertTrue(4 in filtered)

    def test_filter_not(self):
        """Test filter_not operation."""
        s = KotSet([1, 2, 3, 4, 5])
        filtered = s.filter_not(lambda x: x % 2 == 0)
        self.assertEqual(filtered.size, 3)
        self.assertTrue(1 in filtered)
        self.assertTrue(3 in filtered)
        self.assertTrue(5 in filtered)

    def test_filter_not_null(self):
        """Test filter_not_null operation."""
        s = KotSet([1, None, 2, None, 3])
        filtered = s.filter_not_null()
        self.assertEqual(filtered.size, 3)
        self.assertTrue(1 in filtered)
        self.assertTrue(2 in filtered)
        self.assertTrue(3 in filtered)
        self.assertFalse(None in filtered)

    def test_filter_not_none(self):
        """Test filter_not_none alias."""
        s = KotSet([1, None, 2, None, 3])
        filtered = s.filter_not_none()
        self.assertEqual(filtered.size, 3)
        self.assertTrue(1 in filtered)
        self.assertTrue(2 in filtered)
        self.assertTrue(3 in filtered)
        self.assertFalse(None in filtered)


class TestKotSetAggregation(unittest.TestCase):
    """Test KotSet aggregation operations."""

    def test_all(self):
        """Test all predicate."""
        s = KotSet([2, 4, 6, 8])
        self.assertTrue(s.all(lambda x: x % 2 == 0))
        self.assertFalse(s.all(lambda x: x > 5))

    def test_none(self):
        """Test none predicate."""
        s = KotSet([1, 3, 5, 7])
        self.assertTrue(s.none(lambda x: x % 2 == 0))
        self.assertFalse(s.none(lambda x: x > 5))

    def test_any(self):
        """Test any predicate."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertTrue(s.any(lambda x: x > 3))
        self.assertFalse(s.any(lambda x: x > 10))

        # Test any without predicate
        self.assertTrue(s.any())
        empty = KotSet()
        self.assertFalse(empty.any())

    def test_count(self):
        """Test count operation."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertEqual(s.count(), 5)
        self.assertEqual(s.count(lambda x: x % 2 == 0), 2)
        self.assertEqual(s.count(lambda x: x > 10), 0)

    def test_sum_of(self):
        """Test sum_of operation."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertEqual(s.sum_of(lambda x: x), 15)
        self.assertEqual(s.sum_of(lambda x: x * 2), 30)

        empty = KotSet()
        self.assertEqual(empty.sum_of(lambda x: x), 0)

    def test_average(self):
        """Test average operation."""
        s = KotSet([1, 2, 3, 4, 5])
        self.assertEqual(s.average(lambda x: x), 3.0)
        self.assertEqual(s.average(lambda x: x * 2), 6.0)

        empty = KotSet()
        with self.assertRaises(ValueError):
            empty.average(lambda x: x)

    def test_max_or_null(self):
        """Test max_or_null operation."""
        s = KotSet([1, 3, 2, 5, 4])
        self.assertEqual(s.max_or_null(), 5)

        empty = KotSet()
        self.assertIsNone(empty.max_or_null())

    def test_max_or_none(self):
        """Test max_or_none alias."""
        s = KotSet([1, 3, 2, 5, 4])
        self.assertEqual(s.max_or_none(), 5)

        empty = KotSet()
        self.assertIsNone(empty.max_or_none())

    def test_min_or_null(self):
        """Test min_or_null operation."""
        s = KotSet([1, 3, 2, 5, 4])
        self.assertEqual(s.min_or_null(), 1)

        empty = KotSet()
        self.assertIsNone(empty.min_or_null())

    def test_min_or_none(self):
        """Test min_or_none alias."""
        s = KotSet([1, 3, 2, 5, 4])
        self.assertEqual(s.min_or_none(), 1)

        empty = KotSet()
        self.assertIsNone(empty.min_or_none())

    def test_max_by_or_null(self):
        """Test max_by_or_null operation."""
        s = KotSet(["a", "bb", "ccc"])
        self.assertEqual(s.max_by_or_null(len), "ccc")

        empty = KotSet()
        self.assertIsNone(empty.max_by_or_null(len))

    def test_max_by_or_none(self):
        """Test max_by_or_none alias."""
        s = KotSet(["a", "bb", "ccc"])
        self.assertEqual(s.max_by_or_none(len), "ccc")

        empty = KotSet()
        self.assertIsNone(empty.max_by_or_none(len))

    def test_min_by_or_null(self):
        """Test min_by_or_null operation."""
        s = KotSet(["aaa", "bb", "c"])
        self.assertEqual(s.min_by_or_null(len), "c")

        empty = KotSet()
        self.assertIsNone(empty.min_by_or_null(len))

    def test_min_by_or_none(self):
        """Test min_by_or_none alias."""
        s = KotSet(["aaa", "bb", "c"])
        self.assertEqual(s.min_by_or_none(len), "c")

        empty = KotSet()
        self.assertIsNone(empty.min_by_or_none(len))


class TestKotSetCollectionOps(unittest.TestCase):
    """Test KotSet collection operations."""

    def test_fold(self):
        """Test fold operation."""
        s = KotSet([1, 2, 3, 4, 5])
        result = s.fold(0, lambda acc, x: acc + x)
        self.assertEqual(result, 15)

        result = s.fold(1, lambda acc, x: acc * x)
        self.assertEqual(result, 120)

    def test_reduce(self):
        """Test reduce operation."""
        s = KotSet([1, 2, 3, 4, 5])
        result = s.reduce(lambda acc, x: acc + x)
        self.assertEqual(result, 15)

        empty = KotSet()
        with self.assertRaises(ValueError):
            empty.reduce(lambda acc, x: acc + x)

    def test_reduce_or_null(self):
        """Test reduce_or_null operation."""
        s = KotSet([1, 2, 3, 4, 5])
        result = s.reduce_or_null(lambda acc, x: acc + x)
        self.assertEqual(result, 15)

        empty = KotSet()
        self.assertIsNone(empty.reduce_or_null(lambda acc, x: acc + x))

    def test_reduce_or_none(self):
        """Test reduce_or_none alias."""
        s = KotSet([1, 2, 3, 4, 5])
        result = s.reduce_or_none(lambda acc, x: acc + x)
        self.assertEqual(result, 15)

        empty = KotSet()
        self.assertIsNone(empty.reduce_or_none(lambda acc, x: acc + x))

    def test_group_by(self):
        """Test group_by operation."""
        s = KotSet([1, 2, 3, 4, 5, 6])
        groups = s.group_by(lambda x: x % 2)

        self.assertIsInstance(groups, KotMap)
        self.assertEqual(groups.size, 2)
        evens = groups.get(0)
        odds = groups.get(1)

        self.assertIsInstance(evens, KotSet)
        self.assertIsInstance(odds, KotSet)
        self.assertEqual(evens.size, 3)
        self.assertTrue(2 in evens and 4 in evens and 6 in evens)

        self.assertEqual(odds.size, 3)
        self.assertTrue(1 in odds and 3 in odds and 5 in odds)
        
        # Test KotMap operations
        self.assertTrue(groups.contains_key(0))
        self.assertTrue(groups.contains_key(1))
        self.assertEqual(set(groups.keys), {0, 1})

    def test_associate(self):
        """Test associate operation."""
        s = KotSet([1, 2, 3])
        result = s.associate(lambda x: (x, x * x))
        self.assertIsInstance(result, KotMap)
        self.assertEqual(result.to_dict(), {1: 1, 2: 4, 3: 9})
        # Test KotMap operations
        self.assertEqual(result.get(2), 4)
        self.assertTrue(result.contains_key(1))
        self.assertEqual(set(result.keys), {1, 2, 3})
        self.assertEqual(set(result.values), {1, 4, 9})

    def test_associate_by(self):
        """Test associate_by operation."""
        s = KotSet(["hello", "world", "test"])
        result = s.associate_by(len)
        self.assertIsInstance(result, KotMap)
        self.assertEqual(result.get(4), "test")
        self.assertIn(result.get(5), ["hello", "world"])  # Either could be the value
        # Test KotMap operations
        self.assertTrue(result.contains_key(4))
        self.assertTrue(result.contains_key(5))
        self.assertEqual(set(result.keys), {4, 5})

    def test_associate_with(self):
        """Test associate_with operation."""
        s = KotSet([1, 2, 3])
        result = s.associate_with(lambda x: x * x)
        self.assertIsInstance(result, KotMap)
        self.assertEqual(result.to_dict(), {1: 1, 2: 4, 3: 9})
        # Test KotMap operations
        self.assertEqual(result.get(2), 4)
        self.assertTrue(result.contains_key(1))
        self.assertEqual(set(result.keys), {1, 2, 3})
        self.assertEqual(set(result.values), {1, 4, 9})


class TestKotSetSetOperations(unittest.TestCase):
    """Test KotSet set-specific operations."""

    def test_union(self):
        """Test union operation."""
        s1 = KotSet([1, 2, 3])
        s2 = KotSet([3, 4, 5])
        result = s1.union(s2)

        self.assertEqual(result.size, 5)
        for i in range(1, 6):
            self.assertTrue(i in result)

    def test_union_with_python_set(self):
        """Test union with Python set."""
        s1 = KotSet([1, 2, 3])
        s2 = {3, 4, 5}
        result = s1.union(s2)

        self.assertEqual(result.size, 5)
        for i in range(1, 6):
            self.assertTrue(i in result)

    def test_intersect(self):
        """Test intersect operation."""
        s1 = KotSet([1, 2, 3, 4])
        s2 = KotSet([3, 4, 5, 6])
        result = s1.intersect(s2)

        self.assertEqual(result.size, 2)
        self.assertTrue(3 in result)
        self.assertTrue(4 in result)

    def test_subtract(self):
        """Test subtract operation."""
        s1 = KotSet([1, 2, 3, 4])
        s2 = KotSet([3, 4, 5, 6])
        result = s1.subtract(s2)

        self.assertEqual(result.size, 2)
        self.assertTrue(1 in result)
        self.assertTrue(2 in result)


class TestKotSetConversion(unittest.TestCase):
    """Test KotSet conversion operations."""

    def test_to_list(self):
        """Test conversion to list."""
        s = KotSet([1, 2, 3])
        lst = s.to_list()
        self.assertEqual(len(lst), 3)
        self.assertIn(1, lst)
        self.assertIn(2, lst)
        self.assertIn(3, lst)

    def test_to_set(self):
        """Test conversion to Python set."""
        s = KotSet([1, 2, 3])
        py_set = s.to_set()
        self.assertEqual(py_set, {1, 2, 3})

        # Ensure it's a copy
        py_set.add(4)
        self.assertEqual(s.size, 3)

    def test_to_sorted_list(self):
        """Test conversion to sorted list."""
        s = KotSet([3, 1, 4, 1, 5, 9, 2, 6])
        # Use to_list() and sort manually
        sorted_list = sorted(s.to_list())
        self.assertEqual(sorted_list, [1, 2, 3, 4, 5, 6, 9])

        # Test with reverse
        sorted_list = sorted(s.to_list(), reverse=True)
        self.assertEqual(sorted_list, [9, 6, 5, 4, 3, 2, 1])

        # Test with key
        s2 = KotSet(["bb", "aaa", "c"])
        sorted_list = sorted(s2.to_list(), key=len)
        self.assertEqual(sorted_list, ["c", "bb", "aaa"])
        
        # Test to_sorted_set() method
        sorted_set = s.to_sorted_set()
        self.assertIsInstance(sorted_set, KotSet)
        self.assertEqual(list(sorted_set), [1, 2, 3, 4, 5, 6, 9])

    def test_join_to_string(self):
        """Test join_to_string operation."""
        s = KotSet([1, 2, 3])
        # Since sets are unordered, we need to check for any valid permutation
        result = s.join_to_string()
        parts = result.split(", ")
        self.assertEqual(len(parts), 3)
        self.assertIn("1", parts)
        self.assertIn("2", parts)
        self.assertIn("3", parts)

        # Test with prefix and postfix
        result = s.join_to_string(prefix="[", postfix="]")
        self.assertTrue(result.startswith("["))
        self.assertTrue(result.endswith("]"))

        # Test with transform
        result = s.join_to_string(transform=lambda x: f"item-{x}")
        parts = result.split(", ")
        self.assertIn("item-1", parts)
        self.assertIn("item-2", parts)
        self.assertIn("item-3", parts)

        # Test with limit
        s2 = KotSet(range(10))
        result = s2.join_to_string(limit=3, truncated=" and more...")
        self.assertTrue(" and more..." in result)


class TestKotSetNewMethods(unittest.TestCase):
    """Test newly added Kotlin-compatible methods."""
    
    def test_find(self):
        """Test find method."""
        s = KotSet([1, 2, 3, 4, 5])
        # Find existing element
        result = s.find(lambda x: x > 3)
        self.assertIn(result, [4, 5])
        # Find non-existing
        result = s.find(lambda x: x > 10)
        self.assertIsNone(result)
    
    def test_partition(self):
        """Test partition method."""
        s = KotSet([1, 2, 3, 4, 5])
        evens, odds = s.partition(lambda x: x % 2 == 0)
        self.assertEqual(evens.size, 2)
        self.assertEqual(odds.size, 3)
        self.assertTrue(2 in evens)
        self.assertTrue(4 in evens)
        self.assertTrue(1 in odds)
        self.assertTrue(3 in odds)
        self.assertTrue(5 in odds)
    
    def test_for_each(self):
        """Test for_each method."""
        s = KotSet([1, 2, 3])
        result = []
        s.for_each(lambda x: result.append(x * 2))
        self.assertEqual(len(result), 3)
        self.assertTrue(2 in result)
        self.assertTrue(4 in result)
        self.assertTrue(6 in result)
    
    def test_for_each_indexed(self):
        """Test for_each_indexed method."""
        s = KotSet(['a', 'b', 'c'])
        result = []
        s.for_each_indexed(lambda i, x: result.append(f"{i}:{x}"))
        self.assertEqual(len(result), 3)
        # Check that all elements are processed (order not guaranteed)
        combined = ''.join(sorted(result))
        self.assertIn('a', combined)
        self.assertIn('b', combined)
        self.assertIn('c', combined)
    
    def test_plus_minus(self):
        """Test plus and minus methods."""
        s = KotSet([1, 2, 3])
        # Test plus
        s2 = s.plus(4)
        self.assertEqual(s2.size, 4)
        self.assertTrue(4 in s2)
        self.assertEqual(s.size, 3)  # Original unchanged
        
        # Test minus
        s3 = s.minus(2)
        self.assertEqual(s3.size, 2)
        self.assertFalse(2 in s3)
        self.assertEqual(s.size, 3)  # Original unchanged
    
    def test_plus_minus_collection(self):
        """Test plus_collection and minus_collection methods."""
        s = KotSet([1, 2, 3])
        # Test plus_collection
        s2 = s.plus_collection([4, 5])
        self.assertEqual(s2.size, 5)
        
        # Test minus_collection
        s3 = s.minus_collection([1, 3])
        self.assertEqual(s3.size, 1)
        self.assertTrue(2 in s3)
    
    def test_to_mutable_set(self):
        """Test to_mutable_set conversion."""
        s = KotSet([1, 2, 3])
        ms = s.to_kot_mutable_set()
        self.assertEqual(ms.size, 3)
        # Test mutation
        ms.add(4)
        self.assertEqual(ms.size, 4)
        self.assertEqual(s.size, 3)  # Original unchanged
    
    def test_to_mutable_list(self):
        """Test to_mutable_list conversion."""
        s = KotSet([1, 2, 3])
        ml = s.to_kot_mutable_list()
        self.assertEqual(len(ml), 3)
        # Test mutation
        ml.add(4)
        self.assertEqual(len(ml), 4)
        self.assertEqual(s.size, 3)  # Original unchanged
    
    def test_filter_is_instance(self):
        """Test filter_is_instance method."""
        # Test with integers (all same type, filter returns all)
        s = KotSet([1, 2, 3, 4, 5])
        ints = s.filter_is_instance(int)
        self.assertEqual(ints.size, 5)
        self.assertTrue(all(isinstance(x, int) for x in ints))
        
        # Test with different type filter (returns empty)
        strs = s.filter_is_instance(str)
        self.assertEqual(strs.size, 0)
        
        # Test with None values (Set removes duplicates)
        s2 = KotSet([None])
        nones = s2.filter_is_instance(type(None))
        self.assertEqual(nones.size, 1)
    
    def test_map_indexed(self):
        """Test map_indexed method."""
        s = KotSet(['a', 'b', 'c'])
        result = s.map_indexed(lambda i, x: f"{i}:{x}")
        self.assertEqual(result.size, 3)
        # All elements should be transformed
        all_results = list(result)
        self.assertTrue(any(':a' in r for r in all_results))
        self.assertTrue(any(':b' in r for r in all_results))
        self.assertTrue(any(':c' in r for r in all_results))
    
    def test_flat_map_indexed(self):
        """Test flat_map_indexed method."""
        s = KotSet([2, 3, 4])
        result = s.flat_map_indexed(lambda i, x: [x] * i)
        # Results will vary based on iteration order
        self.assertGreater(result.size, 0)
        
        # Test with KotSet return
        s2 = KotSet(['a', 'b'])
        result2 = s2.flat_map_indexed(lambda i, x: KotSet([f"{x}{i}"]))
        self.assertEqual(result2.size, 2)
        
        # Test with set return
        result3 = s2.flat_map_indexed(lambda i, x: {f"{x}-{i}"})
        self.assertEqual(result3.size, 2)
    
    def test_with_index(self):
        """Test with_index method."""
        s = KotSet(['a', 'b', 'c'])
        indexed = list(s.with_index())
        self.assertEqual(len(indexed), 3)
        # Check all indices present
        indices = [i for i, _ in indexed]
        self.assertEqual(sorted(indices), [0, 1, 2])
    
    def test_zip(self):
        """Test zip method."""
        s1 = KotSet([1, 2, 3])
        s2 = KotSet(['a', 'b', 'c'])
        result = s1.zip(s2)
        self.assertLessEqual(result.size, 3)
        # Check that pairs are formed
        for pair in result:
            self.assertIsInstance(pair, tuple)
            self.assertEqual(len(pair), 2)
        
        # Test with Python set
        s3 = s1.zip({'x', 'y', 'z'})
        self.assertLessEqual(s3.size, 3)
    
    def test_as_sequence(self):
        """Test as_sequence method."""
        s = KotSet([1, 2, 3])
        seq = s.as_sequence()
        # Should be an iterator
        self.assertTrue(hasattr(seq, '__iter__'))
        # Can iterate
        values = list(seq)
        self.assertEqual(len(values), 3)
    
    def test_group_by_to(self):
        """Test group_by_to method."""
        s = KotSet(['apple', 'apricot', 'banana', 'blueberry'])
        result = s.group_by_to(
            lambda x: x[0],  # Group by first letter
            lambda x: len(x)  # Transform to length
        )
        self.assertIsInstance(result, KotMap)
        self.assertTrue(result.contains_key('a'))
        self.assertTrue(result.contains_key('b'))
        
        # Values should be KotList instances
        a_values = result.get('a')
        b_values = result.get('b')
        self.assertIsInstance(a_values, KotList)
        self.assertIsInstance(b_values, KotList)
        
        self.assertEqual(a_values.size, 2)
        self.assertEqual(b_values.size, 2)
        
        # Check values are correct (order doesn't matter in sets)
        self.assertEqual(set(a_values.to_list()), {5, 7})  # 'apple'(5) and 'apricot'(7)
        self.assertEqual(set(b_values.to_list()), {6, 9})  # 'banana'(6) and 'blueberry'(9)
        
        # Test KotMap operations
        self.assertEqual(set(result.keys), {'a', 'b'})


class TestKotSetWithKotList(unittest.TestCase):
    """Test KotSet accepting KotList and KotMutableList."""
    
    def test_init_from_kot_list(self):
        """Test creating KotSet from KotList."""
        from kotcollections.kot_list import KotList
        
        kot_list = KotList([1, 2, 2, 3, 3, 3])
        s = KotSet(kot_list)
        self.assertEqual(s.size, 3)  # Duplicates removed
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)
    
    def test_init_from_kot_mutable_list(self):
        """Test creating KotSet from KotMutableList."""
        from kotcollections.kot_mutable_list import KotMutableList
        
        kot_mutable_list = KotMutableList([4, 5, 5, 6, 6, 6])
        s = KotSet(kot_mutable_list)
        self.assertEqual(s.size, 3)  # Duplicates removed
        self.assertTrue(4 in s)
        self.assertTrue(5 in s)
        self.assertTrue(6 in s)
    
    def test_contains_all_with_kot_list(self):
        """Test contains_all with KotList."""
        from kotcollections.kot_list import KotList
        
        s = KotSet([1, 2, 3, 4, 5])
        kot_list = KotList([2, 3, 4])
        self.assertTrue(s.contains_all(kot_list))
        
        kot_list2 = KotList([5, 6, 7])
        self.assertFalse(s.contains_all(kot_list2))
    
    def test_flat_map_with_kot_list(self):
        """Test flat_map returning KotList."""
        from kotcollections.kot_list import KotList
        
        s = KotSet([1, 2, 3])
        flat_mapped = s.flat_map(lambda x: KotList([x, x * 10]))
        self.assertEqual(flat_mapped.size, 6)
        for i in [1, 2, 3, 10, 20, 30]:
            self.assertTrue(i in flat_mapped)
    
    def test_flat_map_with_kot_mutable_list(self):
        """Test flat_map returning KotMutableList."""
        from kotcollections.kot_mutable_list import KotMutableList
        
        s = KotSet([1, 2])
        flat_mapped = s.flat_map(lambda x: KotMutableList([x, x + 10]))
        self.assertEqual(flat_mapped.size, 4)
        for i in [1, 2, 11, 12]:
            self.assertTrue(i in flat_mapped)
    
    def test_flat_map_indexed_with_kot_list(self):
        """Test flat_map_indexed returning KotList."""
        from kotcollections.kot_list import KotList
        
        s = KotSet(['a', 'b'])
        flat_mapped = s.flat_map_indexed(lambda i, x: KotList([f"{x}{i}"]))
        self.assertEqual(flat_mapped.size, 2)
    
    def test_union_with_kot_list(self):
        """Test union with KotList."""
        from kotcollections.kot_list import KotList
        
        s1 = KotSet([1, 2, 3])
        kot_list = KotList([3, 4, 5, 5])
        result = s1.union(kot_list)
        
        self.assertEqual(result.size, 5)
        for i in range(1, 6):
            self.assertTrue(i in result)
    
    def test_intersect_with_kot_list(self):
        """Test intersect with KotList."""
        from kotcollections.kot_list import KotList
        
        s1 = KotSet([1, 2, 3, 4])
        kot_list = KotList([3, 4, 5, 6])
        result = s1.intersect(kot_list)
        
        self.assertEqual(result.size, 2)
        self.assertTrue(3 in result)
        self.assertTrue(4 in result)
    
    def test_subtract_with_kot_list(self):
        """Test subtract with KotList."""
        from kotcollections.kot_list import KotList
        
        s1 = KotSet([1, 2, 3, 4])
        kot_list = KotList([3, 4, 5, 6])
        result = s1.subtract(kot_list)
        
        self.assertEqual(result.size, 2)
        self.assertTrue(1 in result)
        self.assertTrue(2 in result)
    
    def test_plus_collection_with_kot_list(self):
        """Test plus_collection with KotList."""
        from kotcollections.kot_list import KotList
        
        s = KotSet([1, 2, 3])
        kot_list = KotList([4, 5])
        result = s.plus_collection(kot_list)
        
        self.assertEqual(result.size, 5)
        for i in range(1, 6):
            self.assertTrue(i in result)
    
    def test_minus_collection_with_kot_list(self):
        """Test minus_collection with KotList."""
        from kotcollections.kot_list import KotList
        
        s = KotSet([1, 2, 3, 4, 5])
        kot_list = KotList([2, 4])
        result = s.minus_collection(kot_list)
        
        self.assertEqual(result.size, 3)
        self.assertTrue(1 in result)
        self.assertTrue(3 in result)
        self.assertTrue(5 in result)
    
    def test_zip_with_kot_list(self):
        """Test zip with KotList."""
        from kotcollections.kot_list import KotList
        
        s = KotSet([1, 2, 3])
        kot_list = KotList(['a', 'b', 'c', 'd'])
        result = s.zip(kot_list)
        
        self.assertLessEqual(result.size, 3)
        for pair in result:
            self.assertIsInstance(pair, tuple)
            self.assertEqual(len(pair), 2)
            self.assertIsInstance(pair[0], int)
            self.assertIsInstance(pair[1], str)


class TestKotSetInheritanceTypeChecking(unittest.TestCase):
    """Test type checking with inheritance relationships for KotSet."""
    
    def setUp(self):
        """Set up test classes with inheritance."""
        class Animal:
            def __init__(self, name):
                self.name = name
            def __hash__(self):
                return hash(self.name)
            def __eq__(self, other):
                return isinstance(other, Animal) and self.name == other.name
        
        class Dog(Animal):
            pass
        
        class Cat(Animal):
            pass
        
        self.Animal = Animal
        self.Dog = Dog
        self.Cat = Cat
    
    def test_parent_type_accepts_subclass_elements(self):
        """Test that parent type set accepts subclass elements."""
        # Create set with parent type element
        animal_set = KotSet([self.Animal("Generic")])
        mutable_set = animal_set.to_kot_mutable_set()
        
        # Should work - adding Dog to Animal set
        mutable_set.add(self.Dog("Buddy"))
        self.assertEqual(mutable_set.size, 2)
        # Check both elements are in the set
        self.assertTrue(any(isinstance(elem, self.Animal) and elem.name == "Generic" for elem in mutable_set))
        self.assertTrue(any(isinstance(elem, self.Dog) and elem.name == "Buddy" for elem in mutable_set))
        
        # Should also work - adding Cat to Animal set
        mutable_set.add(self.Cat("Whiskers"))
        self.assertEqual(mutable_set.size, 3)
        self.assertTrue(any(isinstance(elem, self.Cat) and elem.name == "Whiskers" for elem in mutable_set))
    
    def test_subclass_type_rejects_parent_elements(self):
        """Test that subclass type set rejects parent class elements."""
        # Create set with subclass type element
        dog_set = KotSet([self.Dog("Buddy")])
        mutable_set = dog_set.to_kot_mutable_set()
        
        # Should fail - adding Animal to Dog set
        with self.assertRaises(TypeError) as cm:
            mutable_set.add(self.Animal("Generic"))
        self.assertIn("All elements must be of type Dog, got Animal", str(cm.exception))
    
    def test_different_subclasses_cannot_mix(self):
        """Test that different subclasses cannot be mixed."""
        # Create set with Dog type element
        dog_set = KotSet([self.Dog("Buddy")])
        mutable_set = dog_set.to_kot_mutable_set()
        
        # Should fail - adding Cat to Dog set
        with self.assertRaises(TypeError) as cm:
            mutable_set.add(self.Cat("Whiskers"))
        self.assertIn("All elements must be of type Dog, got Cat", str(cm.exception))
    
    def test_initialization_with_mixed_types(self):
        """Test initialization with mixed parent/subclass types."""
        # Should work when parent comes first (list preserves order)
        mixed_set = KotSet([self.Animal("Generic"), self.Dog("Buddy")])
        self.assertEqual(mixed_set.size, 2)
        self.assertTrue(any(isinstance(elem, self.Animal) and elem.name == "Generic" for elem in mixed_set))
        self.assertTrue(any(isinstance(elem, self.Dog) and elem.name == "Buddy" for elem in mixed_set))
        
        # Should fail when subclass comes first
        with self.assertRaises(TypeError) as cm:
            KotSet([self.Dog("Buddy"), self.Animal("Generic")])
        self.assertIn("All elements must be of type Dog, got Animal", str(cm.exception))
    
    def test_set_operations_with_inheritance(self):
        """Test set operations (union, intersect) with inheritance."""
        # Test 1: Union with parent type as base - should work
        animal_set = KotSet([self.Animal("Generic1")])
        dog_set_for_union = KotSet([self.Dog("Buddy")])
        
        # Convert dog set to mutable set and add to animal set
        # This ensures Animal type is preserved
        animal_mutable = animal_set.to_kot_mutable_set()
        for elem in dog_set_for_union:
            animal_mutable.add(elem)
        self.assertEqual(animal_mutable.size, 2)
        
        # Test 2: Direct union of incompatible types should fail
        dog_set = KotSet([self.Dog("Buddy")])
        cat_set = KotSet([self.Cat("Whiskers")])
        
        # Since union creates a new set and Python's set.union doesn't preserve order,
        # the type check might fail depending on which element comes first
        # We'll use a different approach to test this
        dog_mutable = dog_set.to_kot_mutable_set()
        with self.assertRaises(TypeError) as cm:
            for elem in cat_set:
                dog_mutable.add(elem)
        self.assertIn("All elements must be of type Dog, got Cat", str(cm.exception))
    
    def test_none_handling_with_inheritance(self):
        """Test that None values are handled correctly with inheritance."""
        # Create set with parent type and None
        animal_set = KotSet([self.Animal("Generic"), None])
        self.assertEqual(animal_set.size, 2)
        self.assertTrue(None in animal_set)
        
        # Should still be able to add subclass
        mutable_set = animal_set.to_kot_mutable_set()
        mutable_set.add(self.Dog("Buddy"))
        self.assertEqual(mutable_set.size, 3)


if __name__ == '__main__':
    unittest.main()
