"""
Tests for Kotlin-style collection interfaces.
"""

import unittest
from kotcollections import (
    # Interfaces
    IKotIterable,
    IKotCollection,
    IKotList,
    IKotSet,
    IKotMap,
    IKotMutableIterable,
    IKotMutableCollection,
    IKotMutableList,
    IKotMutableSet,
    IKotMutableMap,
    # Implementations
    KotList,
    KotMutableList,
    KotSet,
    KotMutableSet,
    KotMap,
    KotMutableMap,
)


class TestInterfaceInstanceCheck(unittest.TestCase):
    """Test that implementations properly implement their interfaces."""

    def test_kot_list_implements_ikot_list(self):
        lst = KotList([1, 2, 3])
        self.assertIsInstance(lst, IKotList)
        self.assertIsInstance(lst, IKotCollection)
        self.assertIsInstance(lst, IKotIterable)

    def test_kot_mutable_list_implements_ikot_mutable_list(self):
        lst = KotMutableList([1, 2, 3])
        self.assertIsInstance(lst, IKotMutableList)
        self.assertIsInstance(lst, IKotMutableCollection)
        self.assertIsInstance(lst, IKotMutableIterable)
        # Should also implement read-only interfaces
        self.assertIsInstance(lst, IKotList)
        self.assertIsInstance(lst, IKotCollection)
        self.assertIsInstance(lst, IKotIterable)

    def test_kot_set_implements_ikot_set(self):
        s = KotSet([1, 2, 3])
        self.assertIsInstance(s, IKotSet)
        self.assertIsInstance(s, IKotCollection)
        self.assertIsInstance(s, IKotIterable)

    def test_kot_mutable_set_implements_ikot_mutable_set(self):
        s = KotMutableSet([1, 2, 3])
        self.assertIsInstance(s, IKotMutableSet)
        self.assertIsInstance(s, IKotMutableCollection)
        self.assertIsInstance(s, IKotMutableIterable)
        # Should also implement read-only interfaces
        self.assertIsInstance(s, IKotSet)
        self.assertIsInstance(s, IKotCollection)
        self.assertIsInstance(s, IKotIterable)

    def test_kot_map_implements_ikot_map(self):
        m = KotMap({"a": 1, "b": 2})
        self.assertIsInstance(m, IKotMap)

    def test_kot_mutable_map_implements_ikot_mutable_map(self):
        m = KotMutableMap({"a": 1, "b": 2})
        self.assertIsInstance(m, IKotMutableMap)
        # Should also implement read-only interface
        self.assertIsInstance(m, IKotMap)


class TestInterfacePolymorphism(unittest.TestCase):
    """Test that interfaces can be used polymorphically."""

    def test_accept_any_list(self):
        """Function accepting IKotList should work with both KotList and KotMutableList."""
        def sum_elements(lst: IKotList[int]) -> int:
            return lst.fold(0, lambda acc, x: acc + x)

        immutable = KotList([1, 2, 3])
        mutable = KotMutableList([1, 2, 3])

        self.assertEqual(sum_elements(immutable), 6)
        self.assertEqual(sum_elements(mutable), 6)

    def test_accept_any_set(self):
        """Function accepting IKotSet should work with both KotSet and KotMutableSet."""
        def count_elements(s: IKotSet[int]) -> int:
            return s.size

        immutable = KotSet([1, 2, 3])
        mutable = KotMutableSet([1, 2, 3])

        self.assertEqual(count_elements(immutable), 3)
        self.assertEqual(count_elements(mutable), 3)

    def test_accept_any_map(self):
        """Function accepting IKotMap should work with both KotMap and KotMutableMap."""
        def get_keys_count(m: IKotMap[str, int]) -> int:
            return m.keys.size

        immutable = KotMap({"a": 1, "b": 2})
        mutable = KotMutableMap({"a": 1, "b": 2})

        self.assertEqual(get_keys_count(immutable), 2)
        self.assertEqual(get_keys_count(mutable), 2)

    def test_accept_any_collection(self):
        """Function accepting IKotCollection should work with KotList and KotSet."""
        def contains_value(col: IKotCollection[int], value: int) -> bool:
            return col.contains(value)

        lst = KotList([1, 2, 3])
        s = KotSet([1, 2, 3])

        self.assertTrue(contains_value(lst, 2))
        self.assertTrue(contains_value(s, 2))
        self.assertFalse(contains_value(lst, 5))
        self.assertFalse(contains_value(s, 5))

    def test_accept_any_iterable(self):
        """Function accepting IKotIterable should work with all collection types."""
        def to_list_manual(iterable: IKotIterable[int]) -> list:
            return list(iterable)

        lst = KotList([1, 2, 3])
        s = KotSet([1, 2, 3])

        self.assertEqual(to_list_manual(lst), [1, 2, 3])
        # Set order may vary, just check length and content
        result = to_list_manual(s)
        self.assertEqual(len(result), 3)
        self.assertEqual(set(result), {1, 2, 3})


class TestInterfaceHierarchy(unittest.TestCase):
    """Test the interface hierarchy relationships."""

    def test_mutable_list_hierarchy(self):
        """KotMutableList should be in the correct hierarchy."""
        lst = KotMutableList()
        # Check full hierarchy
        self.assertIsInstance(lst, IKotMutableList)
        self.assertIsInstance(lst, IKotList)
        self.assertIsInstance(lst, IKotMutableCollection)
        self.assertIsInstance(lst, IKotCollection)
        self.assertIsInstance(lst, IKotMutableIterable)
        self.assertIsInstance(lst, IKotIterable)

    def test_mutable_set_hierarchy(self):
        """KotMutableSet should be in the correct hierarchy."""
        s = KotMutableSet()
        # Check full hierarchy
        self.assertIsInstance(s, IKotMutableSet)
        self.assertIsInstance(s, IKotSet)
        self.assertIsInstance(s, IKotMutableCollection)
        self.assertIsInstance(s, IKotCollection)
        self.assertIsInstance(s, IKotMutableIterable)
        self.assertIsInstance(s, IKotIterable)

    def test_mutable_map_hierarchy(self):
        """KotMutableMap should be in the correct hierarchy."""
        m = KotMutableMap()
        # Check full hierarchy
        self.assertIsInstance(m, IKotMutableMap)
        self.assertIsInstance(m, IKotMap)


class TestInterfaceAbstractMethods(unittest.TestCase):
    """Test that interface abstract methods are properly implemented."""

    def test_list_required_methods(self):
        """KotList should implement all required IKotList methods."""
        lst = KotList([1, 2, 3])

        # IKotIterable
        self.assertTrue(hasattr(lst, '__iter__'))

        # IKotCollection
        self.assertEqual(lst.size, 3)
        self.assertFalse(lst.is_empty())
        self.assertTrue(lst.is_not_empty())
        self.assertTrue(lst.contains(2))
        self.assertTrue(lst.contains_all([1, 2]))

        # IKotList
        self.assertEqual(lst.get(0), 1)
        self.assertIsNone(lst.get_or_null(10))
        self.assertIsNone(lst.get_or_none(10))
        self.assertEqual(lst.index_of(2), 1)
        self.assertEqual(lst.last_index_of(2), 1)
        self.assertEqual(lst.first(), 1)
        self.assertEqual(lst.first_or_null(), 1)
        self.assertEqual(lst.first_or_none(), 1)
        self.assertEqual(lst.last(), 3)
        self.assertEqual(lst.last_or_null(), 3)
        self.assertEqual(lst.last_or_none(), 3)
        self.assertEqual(lst.indices, range(3))
        self.assertEqual(lst.last_index, 2)

    def test_mutable_list_required_methods(self):
        """KotMutableList should implement all required IKotMutableList methods."""
        lst = KotMutableList([1, 2, 3])

        # IKotMutableCollection
        self.assertTrue(lst.add(4))
        self.assertEqual(lst.size, 4)
        self.assertTrue(lst.add_all([5, 6]))
        self.assertEqual(lst.size, 6)
        self.assertTrue(lst.remove(4))
        self.assertNotIn(4, lst)
        self.assertTrue(lst.remove_all([5, 6]))
        # retain_all returns True only if elements were actually removed
        self.assertFalse(lst.retain_all([1, 2, 3]))  # No change, so returns False

        lst = KotMutableList([1, 2, 3])

        # IKotMutableList
        lst.add_at(0, 0)
        self.assertEqual(lst.get(0), 0)
        self.assertTrue(lst.add_all_at(2, [10, 11]))
        old = lst.set(0, 100)
        self.assertEqual(old, 0)
        self.assertEqual(lst.get(0), 100)
        removed = lst.remove_at(0)
        self.assertEqual(removed, 100)

    def test_map_required_methods(self):
        """KotMap should implement all required IKotMap methods."""
        m = KotMap({"a": 1, "b": 2})

        # IKotMap
        self.assertEqual(m.size, 2)
        self.assertFalse(m.is_empty())
        self.assertTrue(m.is_not_empty())
        self.assertTrue(m.contains_key("a"))
        self.assertTrue(m.contains_value(1))
        self.assertEqual(m.get("a"), 1)
        self.assertEqual(m.get_or_default("c", 10), 10)
        self.assertEqual(m.get_or_else("c", lambda: 20), 20)
        self.assertEqual(m.get_value("a"), 1)
        self.assertEqual(m.keys.size, 2)
        self.assertEqual(m.values.size, 2)
        self.assertEqual(m.entries.size, 2)

    def test_mutable_map_required_methods(self):
        """KotMutableMap should implement all required IKotMutableMap methods."""
        m = KotMutableMap({"a": 1})

        # IKotMutableMap
        old = m.put("b", 2)
        self.assertIsNone(old)
        self.assertEqual(m.get("b"), 2)
        m.put_all({"c": 3, "d": 4})
        self.assertEqual(m.size, 4)
        removed = m.remove("d")
        self.assertEqual(removed, 4)
        m.clear()
        self.assertTrue(m.is_empty())


if __name__ == '__main__':
    unittest.main()
