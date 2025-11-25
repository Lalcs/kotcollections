"""
Tests for Kotlin-style collection interfaces.
"""

import pytest
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


class TestInterfaceInstanceCheck:
    """Test that implementations properly implement their interfaces."""

    def test_kot_list_implements_ikot_list(self):
        lst = KotList([1, 2, 3])
        assert isinstance(lst, IKotList)
        assert isinstance(lst, IKotCollection)
        assert isinstance(lst, IKotIterable)

    def test_kot_mutable_list_implements_ikot_mutable_list(self):
        lst = KotMutableList([1, 2, 3])
        assert isinstance(lst, IKotMutableList)
        assert isinstance(lst, IKotMutableCollection)
        assert isinstance(lst, IKotMutableIterable)
        # Should also implement read-only interfaces
        assert isinstance(lst, IKotList)
        assert isinstance(lst, IKotCollection)
        assert isinstance(lst, IKotIterable)

    def test_kot_set_implements_ikot_set(self):
        s = KotSet([1, 2, 3])
        assert isinstance(s, IKotSet)
        assert isinstance(s, IKotCollection)
        assert isinstance(s, IKotIterable)

    def test_kot_mutable_set_implements_ikot_mutable_set(self):
        s = KotMutableSet([1, 2, 3])
        assert isinstance(s, IKotMutableSet)
        assert isinstance(s, IKotMutableCollection)
        assert isinstance(s, IKotMutableIterable)
        # Should also implement read-only interfaces
        assert isinstance(s, IKotSet)
        assert isinstance(s, IKotCollection)
        assert isinstance(s, IKotIterable)

    def test_kot_map_implements_ikot_map(self):
        m = KotMap({"a": 1, "b": 2})
        assert isinstance(m, IKotMap)

    def test_kot_mutable_map_implements_ikot_mutable_map(self):
        m = KotMutableMap({"a": 1, "b": 2})
        assert isinstance(m, IKotMutableMap)
        # Should also implement read-only interface
        assert isinstance(m, IKotMap)


class TestInterfacePolymorphism:
    """Test that interfaces can be used polymorphically."""

    def test_accept_any_list(self):
        """Function accepting IKotList should work with both KotList and KotMutableList."""
        def sum_elements(lst: IKotList[int]) -> int:
            return lst.fold(0, lambda acc, x: acc + x)

        immutable = KotList([1, 2, 3])
        mutable = KotMutableList([1, 2, 3])

        assert sum_elements(immutable) == 6
        assert sum_elements(mutable) == 6

    def test_accept_any_set(self):
        """Function accepting IKotSet should work with both KotSet and KotMutableSet."""
        def count_elements(s: IKotSet[int]) -> int:
            return s.size

        immutable = KotSet([1, 2, 3])
        mutable = KotMutableSet([1, 2, 3])

        assert count_elements(immutable) == 3
        assert count_elements(mutable) == 3

    def test_accept_any_map(self):
        """Function accepting IKotMap should work with both KotMap and KotMutableMap."""
        def get_keys_count(m: IKotMap[str, int]) -> int:
            return m.keys.size

        immutable = KotMap({"a": 1, "b": 2})
        mutable = KotMutableMap({"a": 1, "b": 2})

        assert get_keys_count(immutable) == 2
        assert get_keys_count(mutable) == 2

    def test_accept_any_collection(self):
        """Function accepting IKotCollection should work with KotList and KotSet."""
        def contains_value(col: IKotCollection[int], value: int) -> bool:
            return col.contains(value)

        lst = KotList([1, 2, 3])
        s = KotSet([1, 2, 3])

        assert contains_value(lst, 2)
        assert contains_value(s, 2)
        assert not contains_value(lst, 5)
        assert not contains_value(s, 5)

    def test_accept_any_iterable(self):
        """Function accepting IKotIterable should work with all collection types."""
        def to_list_manual(iterable: IKotIterable[int]) -> list:
            return list(iterable)

        lst = KotList([1, 2, 3])
        s = KotSet([1, 2, 3])

        assert to_list_manual(lst) == [1, 2, 3]
        # Set order may vary, just check length and content
        result = to_list_manual(s)
        assert len(result) == 3
        assert set(result) == {1, 2, 3}


class TestInterfaceHierarchy:
    """Test the interface hierarchy relationships."""

    def test_mutable_list_hierarchy(self):
        """KotMutableList should be in the correct hierarchy."""
        lst = KotMutableList()
        # Check full hierarchy
        assert isinstance(lst, IKotMutableList)
        assert isinstance(lst, IKotList)
        assert isinstance(lst, IKotMutableCollection)
        assert isinstance(lst, IKotCollection)
        assert isinstance(lst, IKotMutableIterable)
        assert isinstance(lst, IKotIterable)

    def test_mutable_set_hierarchy(self):
        """KotMutableSet should be in the correct hierarchy."""
        s = KotMutableSet()
        # Check full hierarchy
        assert isinstance(s, IKotMutableSet)
        assert isinstance(s, IKotSet)
        assert isinstance(s, IKotMutableCollection)
        assert isinstance(s, IKotCollection)
        assert isinstance(s, IKotMutableIterable)
        assert isinstance(s, IKotIterable)

    def test_mutable_map_hierarchy(self):
        """KotMutableMap should be in the correct hierarchy."""
        m = KotMutableMap()
        # Check full hierarchy
        assert isinstance(m, IKotMutableMap)
        assert isinstance(m, IKotMap)


class TestInterfaceAbstractMethods:
    """Test that interface abstract methods are properly implemented."""

    def test_list_required_methods(self):
        """KotList should implement all required IKotList methods."""
        lst = KotList([1, 2, 3])

        # IKotIterable
        assert hasattr(lst, '__iter__')

        # IKotCollection
        assert lst.size == 3
        assert not lst.is_empty()
        assert lst.is_not_empty()
        assert lst.contains(2)
        assert lst.contains_all([1, 2])

        # IKotList
        assert lst.get(0) == 1
        assert lst.get_or_null(10) is None
        assert lst.get_or_none(10) is None
        assert lst.index_of(2) == 1
        assert lst.last_index_of(2) == 1
        assert lst.first() == 1
        assert lst.first_or_null() == 1
        assert lst.first_or_none() == 1
        assert lst.last() == 3
        assert lst.last_or_null() == 3
        assert lst.last_or_none() == 3
        assert lst.indices == range(3)
        assert lst.last_index == 2

    def test_mutable_list_required_methods(self):
        """KotMutableList should implement all required IKotMutableList methods."""
        lst = KotMutableList([1, 2, 3])

        # IKotMutableCollection
        assert lst.add(4)
        assert lst.size == 4
        assert lst.add_all([5, 6])
        assert lst.size == 6
        assert lst.remove(4)
        assert 4 not in lst
        assert lst.remove_all([5, 6])
        # retain_all returns True only if elements were actually removed
        assert not lst.retain_all([1, 2, 3])  # No change, so returns False

        lst = KotMutableList([1, 2, 3])

        # IKotMutableList
        lst.add_at(0, 0)
        assert lst.get(0) == 0
        assert lst.add_all_at(2, [10, 11])
        old = lst.set(0, 100)
        assert old == 0
        assert lst.get(0) == 100
        removed = lst.remove_at(0)
        assert removed == 100

    def test_map_required_methods(self):
        """KotMap should implement all required IKotMap methods."""
        m = KotMap({"a": 1, "b": 2})

        # IKotMap
        assert m.size == 2
        assert not m.is_empty()
        assert m.is_not_empty()
        assert m.contains_key("a")
        assert m.contains_value(1)
        assert m.get("a") == 1
        assert m.get_or_default("c", 10) == 10
        assert m.get_or_else("c", lambda: 20) == 20
        assert m.get_value("a") == 1
        assert m.keys.size == 2
        assert m.values.size == 2
        assert m.entries.size == 2

    def test_mutable_map_required_methods(self):
        """KotMutableMap should implement all required IKotMutableMap methods."""
        m = KotMutableMap({"a": 1})

        # IKotMutableMap
        old = m.put("b", 2)
        assert old is None
        assert m.get("b") == 2
        m.put_all({"c": 3, "d": 4})
        assert m.size == 4
        removed = m.remove("d")
        assert removed == 4
        m.clear()
        assert m.is_empty()
