"""
Unit tests for KotSet class.
"""

import unittest

from kotcollections.kot_set import KotSet


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

        self.assertEqual(len(groups), 2)
        evens = groups[0]
        odds = groups[1]

        self.assertEqual(evens.size, 3)
        self.assertTrue(2 in evens and 4 in evens and 6 in evens)

        self.assertEqual(odds.size, 3)
        self.assertTrue(1 in odds and 3 in odds and 5 in odds)

    def test_associate(self):
        """Test associate operation."""
        s = KotSet([1, 2, 3])
        result = s.associate(lambda x: (x, x * x))
        self.assertEqual(result, {1: 1, 2: 4, 3: 9})

    def test_associate_by(self):
        """Test associate_by operation."""
        s = KotSet(["hello", "world", "test"])
        result = s.associate_by(len)
        self.assertEqual(result[4], "test")
        self.assertIn(result[5], ["hello", "world"])  # Either could be the value

    def test_associate_with(self):
        """Test associate_with operation."""
        s = KotSet([1, 2, 3])
        result = s.associate_with(lambda x: x * x)
        self.assertEqual(result, {1: 1, 2: 4, 3: 9})


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
        sorted_list = s.to_sorted_list()
        self.assertEqual(sorted_list, [1, 2, 3, 4, 5, 6, 9])

        # Test with reverse
        sorted_list = s.to_sorted_list(reverse=True)
        self.assertEqual(sorted_list, [9, 6, 5, 4, 3, 2, 1])

        # Test with key
        s2 = KotSet(["bb", "aaa", "c"])
        sorted_list = s2.to_sorted_list(key=len)
        self.assertEqual(sorted_list, ["c", "bb", "aaa"])

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
