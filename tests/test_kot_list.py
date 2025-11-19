import random
import unittest

from kotcollections import KotList, KotMap, KotSet


class TestKotListBasics(unittest.TestCase):
    def test_init_empty(self):
        lst = KotList()
        self.assertEqual(lst.size, 0)
        self.assertTrue(lst.is_empty())
        self.assertFalse(lst.is_not_empty())

    def test_init_with_elements(self):
        lst = KotList([1, 2, 3])
        self.assertEqual(lst.size, 3)
        self.assertFalse(lst.is_empty())
        self.assertTrue(lst.is_not_empty())

    def test_repr(self):
        lst = KotList([1, 2, 3])
        self.assertEqual(repr(lst), "KotList([1, 2, 3])")

    def test_str(self):
        lst = KotList([1, 2, 3])
        self.assertEqual(str(lst), "[1, 2, 3]")

    def test_eq(self):
        lst1 = KotList([1, 2, 3])
        lst2 = KotList([1, 2, 3])
        lst3 = KotList([1, 2, 4])
        self.assertEqual(lst1, lst2)
        self.assertNotEqual(lst1, lst3)
        self.assertNotEqual(lst1, [1, 2, 3])

    def test_hash(self):
        lst1 = KotList([1, 2, 3])
        lst2 = KotList([1, 2, 3])
        self.assertEqual(hash(lst1), hash(lst2))

    def test_iter(self):
        lst = KotList([1, 2, 3])
        self.assertEqual(list(lst), [1, 2, 3])

    def test_getitem(self):
        lst = KotList([1, 2, 3])
        self.assertEqual(lst[0], 1)
        self.assertEqual(lst[2], 3)

    def test_len(self):
        lst = KotList([1, 2, 3])
        self.assertEqual(len(lst), 3)

    def test_properties(self):
        lst = KotList([1, 2, 3])
        self.assertEqual(lst.indices, range(3))
        self.assertEqual(lst.last_index, 2)

        empty_lst = KotList()
        self.assertEqual(empty_lst.last_index, -1)


class TestKotListAccess(unittest.TestCase):
    def test_get(self):
        lst = KotList([10, 20, 30])
        self.assertEqual(lst.get(0), 10)
        self.assertEqual(lst.get(2), 30)

        with self.assertRaises(IndexError):
            lst.get(-1)
        with self.assertRaises(IndexError):
            lst.get(3)

    def test_get_or_null(self):
        lst = KotList([10, 20, 30])
        self.assertEqual(lst.get_or_null(1), 20)
        self.assertIsNone(lst.get_or_null(-1))
        self.assertIsNone(lst.get_or_null(3))
        
    def test_get_or_none(self):
        lst = KotList([10, 20, 30])
        # Verify alias returns same result as get_or_null
        self.assertEqual(lst.get_or_none(1), lst.get_or_null(1))
        self.assertIsNone(lst.get_or_none(-1))
        self.assertIsNone(lst.get_or_none(3))

    def test_get_or_else(self):
        lst = KotList([10, 20, 30])
        self.assertEqual(lst.get_or_else(1, lambda i: i * 100), 20)
        self.assertEqual(lst.get_or_else(-1, lambda i: i * 100), -100)
        self.assertEqual(lst.get_or_else(3, lambda i: i * 100), 300)

    def test_first(self):
        lst = KotList([10, 20, 30])
        self.assertEqual(lst.first(), 10)

        empty_lst = KotList()
        with self.assertRaises(IndexError):
            empty_lst.first()

    def test_first_predicate(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.first_predicate(lambda x: x > 3), 4)

        with self.assertRaises(ValueError):
            lst.first_predicate(lambda x: x > 10)

    def test_first_or_null(self):
        lst = KotList([10, 20, 30])
        self.assertEqual(lst.first_or_null(), 10)

        empty_lst = KotList()
        self.assertIsNone(empty_lst.first_or_null())
        
    def test_first_or_none(self):
        lst = KotList([10, 20, 30])
        # Verify alias returns same result as first_or_null
        self.assertEqual(lst.first_or_none(), lst.first_or_null())

        empty_lst = KotList()
        self.assertIsNone(empty_lst.first_or_none())

    def test_first_or_null_predicate(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.first_or_null_predicate(lambda x: x > 3), 4)
        self.assertIsNone(lst.first_or_null_predicate(lambda x: x > 10))

    def test_first_or_none_predicate(self):
        lst = KotList([1, 2, 3, 4, 5])
        # Verify alias returns same result as first_or_null_predicate
        self.assertEqual(lst.first_or_none_predicate(lambda x: x > 3), lst.first_or_null_predicate(lambda x: x > 3))
        self.assertEqual(lst.first_or_none_predicate(lambda x: x > 3), 4)
        self.assertIsNone(lst.first_or_none_predicate(lambda x: x > 10))

    def test_last(self):
        lst = KotList([10, 20, 30])
        self.assertEqual(lst.last(), 30)

        empty_lst = KotList()
        with self.assertRaises(IndexError):
            empty_lst.last()

    def test_last_predicate(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.last_predicate(lambda x: x < 4), 3)

        with self.assertRaises(ValueError):
            lst.last_predicate(lambda x: x > 10)

    def test_last_or_null(self):
        lst = KotList([10, 20, 30])
        self.assertEqual(lst.last_or_null(), 30)

        empty_lst = KotList()
        self.assertIsNone(empty_lst.last_or_null())

    def test_last_or_none(self):
        lst = KotList([10, 20, 30])
        # Verify alias returns same result as last_or_null
        self.assertEqual(lst.last_or_none(), lst.last_or_null())
        self.assertEqual(lst.last_or_none(), 30)

        empty_lst = KotList()
        self.assertIsNone(empty_lst.last_or_none())

    def test_last_or_null_predicate(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.last_or_null_predicate(lambda x: x < 4), 3)
        self.assertIsNone(lst.last_or_null_predicate(lambda x: x > 10))

    def test_last_or_none_predicate(self):
        lst = KotList([1, 2, 3, 4, 5])
        # Verify alias returns same result as last_or_null_predicate
        self.assertEqual(lst.last_or_none_predicate(lambda x: x < 4), lst.last_or_null_predicate(lambda x: x < 4))
        self.assertEqual(lst.last_or_none_predicate(lambda x: x < 4), 3)
        self.assertIsNone(lst.last_or_none_predicate(lambda x: x > 10))

    def test_element_at(self):
        lst = KotList([10, 20, 30])
        self.assertEqual(lst.element_at(1), 20)

        with self.assertRaises(IndexError):
            lst.element_at(3)

    def test_element_at_or_else(self):
        lst = KotList([10, 20, 30])
        self.assertEqual(lst.element_at_or_else(1, lambda i: i * 100), 20)
        self.assertEqual(lst.element_at_or_else(3, lambda i: i * 100), 300)

    def test_element_at_or_null(self):
        lst = KotList([10, 20, 30])
        self.assertEqual(lst.element_at_or_null(1), 20)
        self.assertIsNone(lst.element_at_or_null(3))

    def test_element_at_or_none(self):
        lst = KotList([10, 20, 30])
        # Verify alias returns same result as element_at_or_null
        self.assertEqual(lst.element_at_or_none(1), lst.element_at_or_null(1))
        self.assertEqual(lst.element_at_or_none(1), 20)
        self.assertIsNone(lst.element_at_or_none(3))


class TestKotListSearch(unittest.TestCase):
    def test_contains(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertTrue(lst.contains(3))
        self.assertFalse(lst.contains(6))

    def test_contains_all(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertTrue(lst.contains_all([1, 3, 5]))
        self.assertFalse(lst.contains_all([1, 3, 6]))
        self.assertTrue(lst.contains_all([]))
        
        # Test with duplicate elements in input
        self.assertTrue(lst.contains_all([1, 1, 3, 3, 5]))
        
        # Test with all elements not in list
        self.assertFalse(lst.contains_all([6, 7, 8]))

    def test_index_of(self):
        lst = KotList([1, 2, 3, 2, 5])
        self.assertEqual(lst.index_of(2), 1)
        self.assertEqual(lst.index_of(5), 4)
        self.assertEqual(lst.index_of(6), -1)
        
        # Test with element at the beginning
        self.assertEqual(lst.index_of(1), 0)
        
        # Test with empty list
        empty = KotList()
        self.assertEqual(empty.index_of(1), -1)

    def test_last_index_of(self):
        lst = KotList([1, 2, 3, 2, 5])
        self.assertEqual(lst.last_index_of(2), 3)
        self.assertEqual(lst.last_index_of(1), 0)
        self.assertEqual(lst.last_index_of(6), -1)
        
        # Test with single occurrence at the end
        self.assertEqual(lst.last_index_of(5), 4)
        
        # Test with empty list
        empty = KotList()
        self.assertEqual(empty.last_index_of(1), -1)
        
        # Test with all same elements
        same = KotList([2, 2, 2, 2])
        self.assertEqual(same.last_index_of(2), 3)

    def test_index_of_first(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.index_of_first(lambda x: x > 3), 3)
        self.assertEqual(lst.index_of_first(lambda x: x > 10), -1)
        
        # Test finding first element
        self.assertEqual(lst.index_of_first(lambda x: x == 1), 0)
        
        # Test with empty list
        empty = KotList()
        self.assertEqual(empty.index_of_first(lambda x: True), -1)

    def test_index_of_last(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.index_of_last(lambda x: x < 4), 2)
        self.assertEqual(lst.index_of_last(lambda x: x > 10), -1)
        
        # Test finding last element
        self.assertEqual(lst.index_of_last(lambda x: x == 5), 4)
        
        # Test with empty list
        empty = KotList()
        self.assertEqual(empty.index_of_last(lambda x: True), -1)

    def test_binary_search_default(self):
        lst = KotList([1, 3, 5, 7, 9])
        self.assertEqual(lst.binary_search(5), 2)
        self.assertEqual(lst.binary_search(1), 0)
        self.assertEqual(lst.binary_search(9), 4)

        # Not found cases
        self.assertEqual(lst.binary_search(0), -1)
        self.assertEqual(lst.binary_search(4), -3)
        self.assertEqual(lst.binary_search(10), -6)
        
        # Test with element at the end of list matching
        lst2 = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst2.binary_search(5), 4)
        
        # Test with single element list
        single = KotList([42])
        self.assertEqual(single.binary_search(42), 0)
        self.assertEqual(single.binary_search(41), -1)
        self.assertEqual(single.binary_search(43), -2)

    def test_binary_search_comparator(self):
        lst = KotList([(1, 'a'), (3, 'b'), (5, 'c')])

        def comparator(a, b):
            if a[0] < b[0]:
                return -1
            elif a[0] > b[0]:
                return 1
            else:
                return 0

        self.assertEqual(lst.binary_search((3, 'x'), comparator), 1)
        self.assertEqual(lst.binary_search((4, 'x'), comparator), -3)
        
        # Test with reverse sorted list
        reverse_lst = KotList([5, 4, 3, 2, 1])
        
        def reverse_comparator(a, b):
            if a < b:
                return 1  # Reverse order
            elif a > b:
                return -1
            else:
                return 0
        
        # Test finding elements
        self.assertEqual(reverse_lst.binary_search(3, reverse_comparator), 2)
        self.assertEqual(reverse_lst.binary_search(5, reverse_comparator), 0)
        self.assertEqual(reverse_lst.binary_search(1, reverse_comparator), 4)
        
        # Test not finding elements - these cover different branches
        self.assertEqual(reverse_lst.binary_search(0, reverse_comparator), -6)  # Would go after index 5
        self.assertEqual(reverse_lst.binary_search(6, reverse_comparator), -1)  # Would go before index 0
        self.assertEqual(reverse_lst.binary_search(3.5, reverse_comparator), -3)  # Would go between indices
        
        # Additional test cases to ensure all branches are covered
        # Test with list that requires multiple binary search iterations
        long_lst = KotList([10, 8, 6, 4, 2, 0, -2, -4, -6, -8])
        
        # Test finding elements at different positions
        self.assertEqual(long_lst.binary_search(6, reverse_comparator), 2)
        self.assertEqual(long_lst.binary_search(-4, reverse_comparator), 7)
        self.assertEqual(long_lst.binary_search(0, reverse_comparator), 5)
        
        # Test not finding with comparisons that trigger all branches
        self.assertEqual(long_lst.binary_search(5, reverse_comparator), -4)  # Between 6 and 4
        self.assertEqual(long_lst.binary_search(-3, reverse_comparator), -8)  # Between -2 and -4
        
        # Test edge cases with single element and empty list
        single = KotList([42])
        empty = KotList()
        
        # Single element - found
        self.assertEqual(single.binary_search(42, lambda a, b: a - b), 0)
        # Single element - not found (less than)
        self.assertEqual(single.binary_search(40, lambda a, b: a - b), -1)
        # Single element - not found (greater than)
        self.assertEqual(single.binary_search(45, lambda a, b: a - b), -2)
        
        # Empty list
        self.assertEqual(empty.binary_search(10, lambda a, b: a - b), -1)

    def test_binary_search_by(self):
        # Test with objects sorted by a specific property
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age
        
        people = KotList([
            Person("Alice", 25),
            Person("Bob", 30),
            Person("Charlie", 35),
            Person("David", 40)
        ])
        
        # Search by age
        index = people.binary_search_by(30, lambda p: p.age)
        self.assertEqual(index, 1)
        self.assertEqual(people[index].name, "Bob")
        
        # Not found - returns negative insertion point
        self.assertEqual(people.binary_search_by(32, lambda p: p.age), -3)
        self.assertEqual(people.binary_search_by(20, lambda p: p.age), -1)
        self.assertEqual(people.binary_search_by(50, lambda p: p.age), -5)
        
        # Test with custom comparator - list must be sorted by the key
        lst_tuples = KotList([('w', 4), ('x', 3), ('y', 2), ('z', 1)])  # Sorted by first element
        
        def letter_comparator(a, b):
            if a < b:
                return -1
            elif a > b:
                return 1
            return 0
        
        # Search by first element with custom comparator
        index = lst_tuples.binary_search_by('x', lambda t: t[0], letter_comparator)
        self.assertEqual(index, 1)
        
        # Not found with custom comparator
        self.assertEqual(lst_tuples.binary_search_by('v', lambda t: t[0], letter_comparator), -1)
        
        # Test empty list
        empty = KotList()
        self.assertEqual(empty.binary_search_by(10, lambda x: x), -1)
        
        # Test single element
        single = KotList([42])
        self.assertEqual(single.binary_search_by(42, lambda x: x), 0)
        self.assertEqual(single.binary_search_by(40, lambda x: x), -1)
        
        # Test custom comparator with complex search to cover all branches
        sorted_nums = KotList([10, 20, 30, 40, 50, 60, 70, 80, 90])
        
        def custom_cmp(a, b):
            # Custom comparator that ensures we hit all branches
            if a < b:
                return -1
            elif a > b:
                return 1
            return 0
        
        # This should trigger the left = mid + 1 branch (line 243)
        self.assertEqual(sorted_nums.binary_search_by(25, lambda x: x, custom_cmp), -3)
        self.assertEqual(sorted_nums.binary_search_by(35, lambda x: x, custom_cmp), -4)
        self.assertEqual(sorted_nums.binary_search_by(85, lambda x: x, custom_cmp), -9)


class TestKotListTransform(unittest.TestCase):
    def test_map(self):
        lst = KotList([1, 2, 3])
        mapped = lst.map(lambda x: x * 2)
        self.assertEqual(mapped.to_list(), [2, 4, 6])

    def test_map_indexed(self):
        lst = KotList(['a', 'b', 'c'])
        mapped = lst.map_indexed(lambda i, x: f"{i}:{x}")
        self.assertEqual(mapped.to_list(), ['0:a', '1:b', '2:c'])

    def test_map_not_null(self):
        lst = KotList([1, 2, 3, 4])
        mapped = lst.map_not_null(lambda x: x * 2 if x % 2 == 0 else None)
        self.assertEqual(mapped.to_list(), [4, 8])

    def test_map_not_none(self):
        lst = KotList([1, 2, 3, 4])
        # Verify alias returns same result as map_not_null
        mapped_none = lst.map_not_none(lambda x: x * 2 if x % 2 == 0 else None)
        mapped_null = lst.map_not_null(lambda x: x * 2 if x % 2 == 0 else None)
        self.assertEqual(mapped_none.to_list(), mapped_null.to_list())
        self.assertEqual(mapped_none.to_list(), [4, 8])

    def test_flat_map(self):
        lst = KotList([1, 2, 3])
        flat_mapped = lst.flat_map(lambda x: [x, x * 2])
        self.assertEqual(flat_mapped.to_list(), [1, 2, 2, 4, 3, 6])

    def test_flatten(self):
        lst = KotList([[1, 2], [3, 4], [5]])
        flattened = lst.flatten()
        self.assertEqual(flattened.to_list(), [1, 2, 3, 4, 5])
        
        # Test with nested KotLists
        nested = KotList([KotList([1, 2]), KotList([3, 4]), KotList([5])])
        flattened_nested = nested.flatten()
        self.assertEqual(flattened_nested.to_list(), [1, 2, 3, 4, 5])

    def test_associate_with(self):
        lst = KotList(['a', 'bb', 'ccc'])
        assoc = lst.associate_with(lambda x: len(x))
        self.assertIsInstance(assoc, KotMap)
        self.assertEqual(assoc.to_dict(), {'a': 1, 'bb': 2, 'ccc': 3})
        # Test KotMap basic operations
        self.assertEqual(assoc.get('a'), 1)
        self.assertTrue(assoc.contains_key('bb'))
        self.assertEqual(set(assoc.keys), {'a', 'bb', 'ccc'})
        self.assertEqual(set(assoc.values), {1, 2, 3})

    def test_associate_by(self):
        lst = KotList(['a', 'bb', 'ccc'])
        assoc = lst.associate_by(lambda x: len(x))
        self.assertIsInstance(assoc, KotMap)
        self.assertEqual(assoc.to_dict(), {1: 'a', 2: 'bb', 3: 'ccc'})
        # Test KotMap basic operations
        self.assertEqual(assoc.get(1), 'a')
        self.assertTrue(assoc.contains_key(2))
        self.assertEqual(set(assoc.keys), {1, 2, 3})
        self.assertEqual(sorted(assoc.values), ['a', 'bb', 'ccc'])

    def test_associate_by_with_value(self):
        lst = KotList(['a', 'bb', 'ccc'])
        assoc = lst.associate_by_with_value(lambda x: len(x), lambda x: x.upper())
        self.assertIsInstance(assoc, KotMap)
        self.assertEqual(assoc.to_dict(), {1: 'A', 2: 'BB', 3: 'CCC'})
        # Test KotMap basic operations
        self.assertEqual(assoc.get(1), 'A')
        self.assertTrue(assoc.contains_key(3))
        self.assertEqual(set(assoc.keys), {1, 2, 3})
        self.assertEqual(sorted(assoc.values), ['A', 'BB', 'CCC'])


class TestKotListFilter(unittest.TestCase):
    def test_filter(self):
        lst = KotList([1, 2, 3, 4, 5])
        filtered = lst.filter(lambda x: x % 2 == 0)
        self.assertEqual(filtered.to_list(), [2, 4])

    def test_filter_indexed(self):
        lst = KotList(['a', 'b', 'c', 'd'])
        filtered = lst.filter_indexed(lambda i, x: i % 2 == 0)
        self.assertEqual(filtered.to_list(), ['a', 'c'])

    def test_filter_not(self):
        lst = KotList([1, 2, 3, 4, 5])
        filtered = lst.filter_not(lambda x: x % 2 == 0)
        self.assertEqual(filtered.to_list(), [1, 3, 5])

    def test_filter_not_null(self):
        # In Kotlin, nullable types would be List<Int?>, but we don't have Optional[T] in Python
        # So we'll test with a list that doesn't contain None
        lst = KotList([1, 2, 3, 4, 5])
        filtered = lst.filter_not_null()
        self.assertEqual(filtered.to_list(), [1, 2, 3, 4, 5])

    def test_filter_not_none(self):
        # Verify alias returns same result as filter_not_null
        lst = KotList([1, 2, 3, 4, 5])
        filtered_none = lst.filter_not_none()
        filtered_null = lst.filter_not_null()
        self.assertEqual(filtered_none.to_list(), filtered_null.to_list())
        self.assertEqual(filtered_none.to_list(), [1, 2, 3, 4, 5])


    def test_partition(self):
        lst = KotList([1, 2, 3, 4, 5])
        evens, odds = lst.partition(lambda x: x % 2 == 0)
        self.assertEqual(evens.to_list(), [2, 4])
        self.assertEqual(odds.to_list(), [1, 3, 5])


class TestKotListTesting(unittest.TestCase):
    def test_any(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertTrue(lst.any(lambda x: x > 3))
        self.assertFalse(lst.any(lambda x: x > 10))

        # Without predicate
        self.assertTrue(lst.any())
        self.assertFalse(KotList().any())

    def test_all(self):
        lst = KotList([2, 4, 6, 8])
        self.assertTrue(lst.all(lambda x: x % 2 == 0))
        self.assertFalse(lst.all(lambda x: x > 5))

    def test_none(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertTrue(lst.none(lambda x: x > 10))
        self.assertFalse(lst.none(lambda x: x > 3))

        # Without predicate
        self.assertFalse(lst.none())
        self.assertTrue(KotList().none())


class TestKotListAggregation(unittest.TestCase):
    def test_count(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.count(), 5)
        self.assertEqual(lst.count(lambda x: x % 2 == 0), 2)

    def test_sum_of(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.sum_of(lambda x: x), 15)
        self.assertEqual(lst.sum_of(lambda x: x * 2), 30)

    def test_max_or_null(self):
        lst = KotList([3, 1, 4, 1, 5])
        self.assertEqual(lst.max_or_null(), 5)

        empty_lst = KotList()
        self.assertIsNone(empty_lst.max_or_null())

    def test_max_or_none(self):
        lst = KotList([3, 1, 4, 1, 5])
        # Verify alias returns same result as max_or_null
        self.assertEqual(lst.max_or_none(), lst.max_or_null())
        self.assertEqual(lst.max_or_none(), 5)

        empty_lst = KotList()
        self.assertIsNone(empty_lst.max_or_none())

    def test_min_or_null(self):
        lst = KotList([3, 1, 4, 1, 5])
        self.assertEqual(lst.min_or_null(), 1)

        empty_lst = KotList()
        self.assertIsNone(empty_lst.min_or_null())

    def test_min_or_none(self):
        lst = KotList([3, 1, 4, 1, 5])
        # Verify alias returns same result as min_or_null
        self.assertEqual(lst.min_or_none(), lst.min_or_null())
        self.assertEqual(lst.min_or_none(), 1)

        empty_lst = KotList()
        self.assertIsNone(empty_lst.min_or_none())

    def test_max_by_or_null(self):
        lst = KotList(['a', 'bbb', 'cc'])
        self.assertEqual(lst.max_by_or_null(lambda x: len(x)), 'bbb')

        empty_lst = KotList()
        self.assertIsNone(empty_lst.max_by_or_null(lambda x: x))

    def test_max_by_or_none(self):
        lst = KotList(['a', 'bbb', 'cc'])
        # Verify alias returns same result as max_by_or_null
        self.assertEqual(lst.max_by_or_none(lambda x: len(x)), lst.max_by_or_null(lambda x: len(x)))
        self.assertEqual(lst.max_by_or_none(lambda x: len(x)), 'bbb')

        empty_lst = KotList()
        self.assertIsNone(empty_lst.max_by_or_none(lambda x: x))

    def test_min_by_or_null(self):
        lst = KotList(['a', 'bbb', 'cc'])
        self.assertEqual(lst.min_by_or_null(lambda x: len(x)), 'a')

        empty_lst = KotList()
        self.assertIsNone(empty_lst.min_by_or_null(lambda x: x))

    def test_min_by_or_none(self):
        lst = KotList(['a', 'bbb', 'cc'])
        # Verify alias returns same result as min_by_or_null
        self.assertEqual(lst.min_by_or_none(lambda x: len(x)), lst.min_by_or_null(lambda x: len(x)))
        self.assertEqual(lst.min_by_or_none(lambda x: len(x)), 'a')

        empty_lst = KotList()
        self.assertIsNone(empty_lst.min_by_or_none(lambda x: x))

    def test_average(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.average(), 3.0)

        empty_lst = KotList()
        import math
        result = empty_lst.average()
        self.assertTrue(math.isnan(result))  # Kotlin-compatible: returns NaN for empty


class TestKotListSorting(unittest.TestCase):
    def test_sorted(self):
        lst = KotList([3, 1, 4, 1, 5])
        sorted_lst = lst.sorted()
        self.assertEqual(sorted_lst.to_list(), [1, 1, 3, 4, 5])

        # With key
        lst_str = KotList(['bb', 'aaa', 'c'])
        sorted_by_len = lst_str.sorted(key=len)
        self.assertEqual(sorted_by_len.to_list(), ['c', 'bb', 'aaa'])

        # Reverse
        sorted_desc = lst.sorted(reverse=True)
        self.assertEqual(sorted_desc.to_list(), [5, 4, 3, 1, 1])

    def test_sorted_descending(self):
        lst = KotList([3, 1, 4, 1, 5])
        sorted_desc = lst.sorted_descending()
        self.assertEqual(sorted_desc.to_list(), [5, 4, 3, 1, 1])

    def test_sorted_by(self):
        lst = KotList(['bb', 'aaa', 'c'])
        sorted_lst = lst.sorted_by(lambda x: len(x))
        self.assertEqual(sorted_lst.to_list(), ['c', 'bb', 'aaa'])

    def test_sorted_by_descending(self):
        lst = KotList(['bb', 'aaa', 'c'])
        sorted_lst = lst.sorted_by_descending(lambda x: len(x))
        self.assertEqual(sorted_lst.to_list(), ['aaa', 'bb', 'c'])

    def test_sorted_with(self):
        # Test with custom comparator - sort by absolute value
        lst = KotList([-5, -1, 3, -2, 4])
        sorted_lst = lst.sorted_with(lambda a, b: abs(a) - abs(b))
        self.assertEqual(sorted_lst.to_list(), [-1, -2, 3, 4, -5])
        
        # Test with string length comparison
        lst_str = KotList(['aaa', 'bb', 'cccc', 'd'])
        sorted_str = lst_str.sorted_with(lambda a, b: len(a) - len(b))
        self.assertEqual(sorted_str.to_list(), ['d', 'bb', 'aaa', 'cccc'])
        
        # Test reverse comparison
        lst_int = KotList([3, 1, 4, 1, 5])
        sorted_desc = lst_int.sorted_with(lambda a, b: b - a)
        self.assertEqual(sorted_desc.to_list(), [5, 4, 3, 1, 1])

    def test_reversed(self):
        lst = KotList([1, 2, 3, 4, 5])
        reversed_lst = lst.reversed()
        self.assertEqual(reversed_lst.to_list(), [5, 4, 3, 2, 1])

    def test_shuffled(self):
        lst = KotList([1, 2, 3, 4, 5])
        # Use a fixed seed for reproducible test
        rng = random.Random(42)
        shuffled = lst.shuffled(rng)
        # Check that all elements are present
        self.assertEqual(sorted(shuffled.to_list()), [1, 2, 3, 4, 5])
        # It's unlikely (but possible) that shuffled equals original

        # Test without random instance
        shuffled2 = lst.shuffled()
        self.assertEqual(sorted(shuffled2.to_list()), [1, 2, 3, 4, 5])


class TestKotListGrouping(unittest.TestCase):
    def test_group_by(self):
        lst = KotList([1, 2, 3, 4, 5, 6])
        grouped = lst.group_by(lambda x: x % 2)
        self.assertIsInstance(grouped, KotMap)
        self.assertEqual(grouped.get(0).to_list(), [2, 4, 6])
        self.assertEqual(grouped.get(1).to_list(), [1, 3, 5])
        # Test KotMap operations
        self.assertTrue(grouped.contains_key(0))
        self.assertTrue(grouped.contains_key(1))
        self.assertEqual(set(grouped.keys), {0, 1})
        # Test that values are KotList instances
        self.assertIsInstance(grouped.get(0), KotList)
        self.assertIsInstance(grouped.get(1), KotList)

    def test_group_by_with_value(self):
        lst = KotList(['a', 'bb', 'ccc', 'dd', 'e'])
        grouped = lst.group_by_with_value(lambda x: len(x), lambda x: x.upper())
        self.assertIsInstance(grouped, KotMap)
        self.assertEqual(grouped.get(1).to_list(), ['A', 'E'])
        self.assertEqual(grouped.get(2).to_list(), ['BB', 'DD'])
        self.assertEqual(grouped.get(3).to_list(), ['CCC'])
        # Test KotMap operations
        self.assertTrue(grouped.contains_key(1))
        self.assertTrue(grouped.contains_key(2))
        self.assertTrue(grouped.contains_key(3))
        self.assertEqual(set(grouped.keys), {1, 2, 3})
        # Test that values are KotList instances
        self.assertIsInstance(grouped.get(1), KotList)
        self.assertIsInstance(grouped.get(2), KotList)
        self.assertIsInstance(grouped.get(3), KotList)

    def test_chunked(self):
        lst = KotList([1, 2, 3, 4, 5, 6, 7])
        chunked = lst.chunked(3)
        self.assertEqual(len(chunked), 3)
        self.assertEqual(chunked[0].to_list(), [1, 2, 3])
        self.assertEqual(chunked[1].to_list(), [4, 5, 6])
        self.assertEqual(chunked[2].to_list(), [7])

        with self.assertRaises(ValueError):
            lst.chunked(0)

    def test_chunked_transform(self):
        lst = KotList([1, 2, 3, 4, 5, 6, 7])
        sums = lst.chunked_transform(3, lambda chunk: sum(chunk.to_list()))
        self.assertEqual(sums.to_list(), [6, 15, 7])

        with self.assertRaises(ValueError):
            lst.chunked_transform(0, lambda x: x)

    def test_windowed(self):
        lst = KotList([1, 2, 3, 4, 5])

        # Basic windowing
        windows = lst.windowed(3)
        self.assertEqual(len(windows), 3)
        self.assertEqual(windows[0].to_list(), [1, 2, 3])
        self.assertEqual(windows[1].to_list(), [2, 3, 4])
        self.assertEqual(windows[2].to_list(), [3, 4, 5])

        # With step
        windows_step = lst.windowed(3, step=2)
        self.assertEqual(len(windows_step), 2)
        self.assertEqual(windows_step[0].to_list(), [1, 2, 3])
        self.assertEqual(windows_step[1].to_list(), [3, 4, 5])

        # With partial windows
        windows_partial = lst.windowed(3, step=2, partial_windows=True)
        self.assertEqual(len(windows_partial), 3)
        self.assertEqual(windows_partial[2].to_list(), [5])
        
        # Test case where partial_windows=False and last window is smaller
        # This should trigger the break statement (line 428->424)
        lst2 = KotList([1, 2, 3, 4, 5, 6, 7])
        windows_no_partial = lst2.windowed(3, step=3, partial_windows=False)
        self.assertEqual(len(windows_no_partial), 2)  # Only [1,2,3] and [4,5,6], not [7]
        self.assertEqual(windows_no_partial[0].to_list(), [1, 2, 3])
        self.assertEqual(windows_no_partial[1].to_list(), [4, 5, 6])
        
        # Edge case: empty list
        empty = KotList()
        self.assertEqual(empty.windowed(3).to_list(), [])

        # Error cases
        with self.assertRaises(ValueError):
            lst.windowed(0)
        with self.assertRaises(ValueError):
            lst.windowed(3, step=0)


class TestKotListCollectionOps(unittest.TestCase):
    def test_distinct(self):
        lst = KotList([1, 2, 2, 3, 3, 3, 4])
        distinct = lst.distinct()
        self.assertEqual(distinct.to_list(), [1, 2, 3, 4])

    def test_distinct_by(self):
        lst = KotList(['a', 'aa', 'b', 'bb', 'ccc'])
        distinct = lst.distinct_by(lambda x: len(x))
        self.assertEqual(distinct.to_list(), ['a', 'aa', 'ccc'])

    def test_intersect(self):
        lst1 = KotList([1, 2, 3, 4, 5])
        lst2 = [3, 4, 5, 6, 7]
        intersection = lst1.intersect(lst2)
        from kotcollections import KotSet
        self.assertIsInstance(intersection, KotSet)
        self.assertEqual(set(intersection.to_list()), {3, 4, 5})

    def test_union(self):
        lst1 = KotList([1, 2, 3])
        lst2 = [3, 4, 5]
        union = lst1.union(lst2)
        from kotcollections import KotSet
        self.assertIsInstance(union, KotSet)
        self.assertEqual(set(union.to_list()), {1, 2, 3, 4, 5})

    def test_plus(self):
        lst = KotList([1, 2, 3])

        # Plus single element
        plus_single = lst.plus(4)
        self.assertEqual(plus_single.to_list(), [1, 2, 3, 4])

        # Plus iterable
        plus_multiple = lst.plus([4, 5])
        self.assertEqual(plus_multiple.to_list(), [1, 2, 3, 4, 5])

        # Plus string (should treat as single element)
        lst_str = KotList(['a', 'b'])
        plus_str = lst_str.plus('cd')
        self.assertEqual(plus_str.to_list(), ['a', 'b', 'cd'])

    def test_minus(self):
        lst = KotList([1, 2, 3, 4, 5])

        # Minus single element
        minus_single = lst.minus(3)
        self.assertEqual(minus_single.to_list(), [1, 2, 4, 5])

        # Minus non-existent element
        minus_none = lst.minus(6)
        self.assertEqual(minus_none.to_list(), [1, 2, 3, 4, 5])

        # Minus multiple elements
        minus_multiple = lst.minus([2, 4])
        self.assertEqual(minus_multiple.to_list(), [1, 3, 5])

    def test_sub_list(self):
        lst = KotList([1, 2, 3, 4, 5])
        sub = lst.sub_list(1, 4)
        self.assertEqual(sub.to_list(), [2, 3, 4])


class TestKotListZipOps(unittest.TestCase):
    def test_zip(self):
        lst1 = KotList([1, 2, 3])
        lst2 = ['a', 'b', 'c', 'd']
        zipped = lst1.zip(lst2)
        self.assertEqual(zipped.to_list(), [(1, 'a'), (2, 'b'), (3, 'c')])

    def test_zip_transform(self):
        lst1 = KotList([1, 2, 3])
        lst2 = [10, 20, 30]
        transformed = lst1.zip_transform(lst2, lambda a, b: a + b)
        self.assertEqual(transformed.to_list(), [11, 22, 33])

    def test_unzip(self):
        lst = KotList([(1, 'a'), (2, 'b'), (3, 'c')])
        first, second = lst.unzip()
        self.assertEqual(first.to_list(), [1, 2, 3])
        self.assertEqual(second.to_list(), ['a', 'b', 'c'])

        # Empty list
        empty = KotList()
        first_empty, second_empty = empty.unzip()
        self.assertEqual(first_empty.to_list(), [])
        self.assertEqual(second_empty.to_list(), [])


class TestKotListAccumulation(unittest.TestCase):
    def test_fold(self):
        lst = KotList([1, 2, 3, 4])
        result = lst.fold(0, lambda acc, x: acc + x)
        self.assertEqual(result, 10)

        # With different initial value
        result2 = lst.fold(10, lambda acc, x: acc + x)
        self.assertEqual(result2, 20)

    def test_reduce(self):
        lst = KotList([1, 2, 3, 4])
        result = lst.reduce(lambda a, b: a + b)
        self.assertEqual(result, 10)

        # Empty list
        empty = KotList()
        with self.assertRaises(ValueError):
            empty.reduce(lambda a, b: a + b)

    def test_scan(self):
        lst = KotList([1, 2, 3, 4])
        scanned = lst.scan(0, lambda acc, x: acc + x)
        self.assertEqual(scanned.to_list(), [0, 1, 3, 6, 10])


class TestKotListIteration(unittest.TestCase):
    def test_for_each(self):
        lst = KotList([1, 2, 3])
        result = []
        lst.for_each(lambda x: result.append(x * 2))
        self.assertEqual(result, [2, 4, 6])

    def test_for_each_indexed(self):
        lst = KotList(['a', 'b', 'c'])
        result = []
        lst.for_each_indexed(lambda i, x: result.append(f"{i}:{x}"))
        self.assertEqual(result, ['0:a', '1:b', '2:c'])

    def test_on_each(self):
        lst = KotList([1, 2, 3])
        result = []
        returned = lst.on_each(lambda x: result.append(x * 2))
        self.assertEqual(result, [2, 4, 6])
        self.assertEqual(returned, lst)  # Should return self


class TestKotListConversion(unittest.TestCase):
    def test_to_list(self):
        lst = KotList([1, 2, 3])
        python_list = lst.to_list()
        self.assertEqual(python_list, [1, 2, 3])
        self.assertIsInstance(python_list, list)

        # Ensure it's a copy
        python_list.append(4)
        self.assertEqual(lst.size, 3)

    def test_to_mutable_list(self):
        from kotcollections import KotMutableList
        lst = KotList([1, 2, 3])
        mutable = lst.to_kot_mutable_list()
        self.assertIsInstance(mutable, KotMutableList)
        self.assertEqual(mutable.to_list(), [1, 2, 3])

    def test_to_set(self):
        lst = KotList([1, 2, 2, 3, 3, 3])
        python_set = lst.to_set()
        self.assertEqual(python_set, {1, 2, 3})
        self.assertIsInstance(python_set, set)
        
        # Test to_kot_set separately
        from kotcollections.kot_set import KotSet
        kot_set = lst.to_kot_set()
        self.assertEqual(kot_set._elements, {1, 2, 3})
        self.assertIsInstance(kot_set, KotSet)

    def test_to_mutable_set(self):
        from kotcollections.kot_mutable_set import KotMutableSet
        lst = KotList([1, 2, 2, 3, 3, 3])
        kot_mutable_set = lst.to_kot_mutable_set()
        self.assertEqual(kot_mutable_set._elements, {1, 2, 3})
        self.assertIsInstance(kot_mutable_set, KotMutableSet)


class TestKotListJoinToString(unittest.TestCase):
    def test_join_to_string_basic(self):
        lst = KotList([1, 2, 3])
        result = lst.join_to_string()
        self.assertEqual(result, "1, 2, 3")

    def test_join_to_string_with_params(self):
        lst = KotList([1, 2, 3])
        result = lst.join_to_string(separator=" | ", prefix="[", postfix="]")
        self.assertEqual(result, "[1 | 2 | 3]")

    def test_join_to_string_with_limit(self):
        lst = KotList([1, 2, 3, 4, 5])
        result = lst.join_to_string(limit=3, truncated="...")
        self.assertEqual(result, "1, 2, 3...")

    def test_join_to_string_with_transform(self):
        lst = KotList([1, 2, 3])
        result = lst.join_to_string(transform=lambda x: f"n{x}")
        self.assertEqual(result, "n1, n2, n3")

    def test_join_to_string_empty(self):
        lst = KotList()
        result = lst.join_to_string(prefix="[", postfix="]")
        self.assertEqual(result, "[]")


class TestKotListTypeChecking(unittest.TestCase):
    def test_type_checking_init(self):
        # Same type elements - should work
        lst = KotList([1, 2, 3])
        self.assertEqual(lst.to_list(), [1, 2, 3])
        
        # Mixed types - should raise TypeError
        with self.assertRaises(TypeError) as cm:
            KotList([1, 'a', 2])
        self.assertIn("Cannot add element of type 'str' to KotList[int]", str(cm.exception))
    
    def test_nested_kot_lists(self):
        # Nested KotLists - should work
        nested = KotList([KotList([1, 2]), KotList([3, 4])])
        self.assertEqual(len(nested), 2)
        
        # Mixed KotList and other types - should raise TypeError
        with self.assertRaises(TypeError) as cm:
            KotList([KotList([1, 2]), [3, 4]])
        self.assertIn("Cannot add element of type 'list' to KotList[KotList]", str(cm.exception))
    
    def test_empty_list_type_setting(self):
        # Empty list should accept the first element's type
        lst = KotList()
        self.assertEqual(lst.to_list(), [])
        
        # Type is not set yet
        self.assertIsNone(lst._element_type)
    
    def test_kot_list_in_different_type_list(self):
        # Try to add KotList to a list of different type
        lst = KotList([1, 2, 3])
        
        # Try to add a KotList - should raise TypeError
        with self.assertRaises(TypeError) as cm:
            lst._check_type(KotList([4, 5]))
        self.assertIn("Cannot add element of type 'KotList' to KotList", str(cm.exception))
    
    def test_flatten_with_non_iterable(self):
        # Test flatten with non-iterable elements (strings are iterable, so use numbers)
        # Since we have type checking, we can only test with KotList elements
        lst = KotList([KotList([1]), KotList([2, 3])])
        flattened = lst.flatten()
        self.assertEqual(flattened.to_list(), [1, 2, 3])
    
    def test_filter_is_instance_same_type(self):
        # Since we enforce type safety, filter_is_instance will only work with same type
        lst = KotList([1, 2, 3, 4, 5])
        filtered = lst.filter_is_instance(int)
        self.assertEqual(filtered.to_list(), [1, 2, 3, 4, 5])
    
    def test_empty_list_then_add_kot_list(self):
        # Test adding KotList as first element to empty list (covers line 39)
        from kotcollections import KotMutableList
        empty = KotMutableList()
        kot_element = KotList([1, 2, 3])
        empty.add(kot_element)
        self.assertEqual(empty._element_type, KotList)
        
        # Can add more KotLists
        empty.add(KotList([4, 5, 6]))
        self.assertEqual(len(empty), 2)
    
    def test_flatten_with_non_iterable_in_kot_list(self):
        # Test flatten with non-iterable elements (covers line 227)
        # Numbers are not iterable (except strings)
        lst = KotList([1, 2, 3])
        flattened = lst.flatten()
        self.assertEqual(flattened.to_list(), [1, 2, 3])
        
        # Test with other non-iterable types
        lst2 = KotList([True, False, True])
        flattened2 = lst2.flatten()
        self.assertEqual(flattened2.to_list(), [True, False, True])
    
    def test_inheritance_type_checking(self):
        """Test type checking with inheritance relationships"""
        # Define test classes with inheritance
        class Animal:
            def __init__(self, name):
                self.name = name
        
        class Dog(Animal):
            pass
        
        class Cat(Animal):
            pass
        
        # Test 1: Parent type collection accepts subclass elements
        animal_list = KotList([Animal("Generic")])
        # Should work - adding Dog to Animal list
        animal_list_mutable = animal_list.to_kot_mutable_list()
        animal_list_mutable.add(Dog("Buddy"))
        self.assertEqual(len(animal_list_mutable), 2)
        self.assertIsInstance(animal_list_mutable[0], Animal)
        self.assertIsInstance(animal_list_mutable[1], Dog)
        
        # Test 2: Subclass type collection rejects parent class elements
        dog_list = KotList([Dog("Buddy")])
        dog_list_mutable = dog_list.to_kot_mutable_list()
        with self.assertRaises(TypeError) as cm:
            dog_list_mutable.add(Animal("Generic"))
        self.assertIn("Cannot add element of type 'Animal' to KotList[Dog]", str(cm.exception))
        
        # Test 3: Different subclasses cannot be mixed
        with self.assertRaises(TypeError) as cm:
            dog_list_mutable.add(Cat("Whiskers"))
        self.assertIn("Cannot add element of type 'Cat' to KotList[Dog]", str(cm.exception))
        
        # Test 4: Initialization with mixed parent/subclass fails when subclass comes first
        with self.assertRaises(TypeError) as cm:
            KotList([Dog("Buddy"), Animal("Generic")])
        self.assertIn("Cannot add element of type 'Animal' to KotList[Dog]", str(cm.exception))
        
        # Test 5: Initialization with mixed parent/subclass works when parent comes first
        mixed_list = KotList([Animal("Generic"), Dog("Buddy")])
        self.assertEqual(len(mixed_list), 2)
        self.assertIsInstance(mixed_list[0], Animal)
        self.assertIsInstance(mixed_list[1], Dog)


class TestKotListNewElementRetrieval(unittest.TestCase):
    def test_component_methods(self):
        lst = KotList([10, 20, 30, 40, 50])
        self.assertEqual(lst.component1(), 10)
        self.assertEqual(lst.component2(), 20)
        self.assertEqual(lst.component3(), 30)
        self.assertEqual(lst.component4(), 40)
        self.assertEqual(lst.component5(), 50)
        
        # Test with fewer elements
        short_lst = KotList([1, 2])
        self.assertEqual(short_lst.component1(), 1)
        self.assertEqual(short_lst.component2(), 2)
        with self.assertRaises(IndexError):
            short_lst.component3()
    
    def test_single(self):
        # Test with single element
        single_lst = KotList([42])
        self.assertEqual(single_lst.single(), 42)
        
        # Test with empty list
        empty_lst = KotList()
        with self.assertRaises(ValueError) as cm:
            empty_lst.single()
        self.assertIn("List is empty", str(cm.exception))
        
        # Test with multiple elements
        multi_lst = KotList([1, 2, 3])
        with self.assertRaises(ValueError) as cm:
            multi_lst.single()
        self.assertIn("List has more than one element", str(cm.exception))
    
    def test_single_or_null(self):
        # Test with single element
        single_lst = KotList([42])
        self.assertEqual(single_lst.single_or_null(), 42)
        self.assertEqual(single_lst.single_or_none(), 42)  # Test alias
        
        # Test with empty list
        empty_lst = KotList()
        self.assertIsNone(empty_lst.single_or_null())
        self.assertIsNone(empty_lst.single_or_none())
        
        # Test with multiple elements
        multi_lst = KotList([1, 2, 3])
        self.assertIsNone(multi_lst.single_or_null())
        self.assertIsNone(multi_lst.single_or_none())
    
    def test_single_predicate(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test finding single element
        self.assertEqual(lst.single_predicate(lambda x: x == 3), 3)
        
        # Test no matching element
        with self.assertRaises(ValueError) as cm:
            lst.single_predicate(lambda x: x == 10)
        self.assertIn("No element matching predicate found", str(cm.exception))
        
        # Test multiple matching elements
        with self.assertRaises(ValueError) as cm:
            lst.single_predicate(lambda x: x > 3)
        self.assertIn("More than one element matching predicate found", str(cm.exception))
    
    def test_single_or_null_predicate(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test finding single element
        self.assertEqual(lst.single_or_null_predicate(lambda x: x == 3), 3)
        self.assertEqual(lst.single_or_none_predicate(lambda x: x == 3), 3)  # Test alias
        
        # Test no matching element
        self.assertIsNone(lst.single_or_null_predicate(lambda x: x == 10))
        self.assertIsNone(lst.single_or_none_predicate(lambda x: x == 10))
        
        # Test multiple matching elements
        self.assertIsNone(lst.single_or_null_predicate(lambda x: x > 3))
        self.assertIsNone(lst.single_or_none_predicate(lambda x: x > 3))
    
    def test_random(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test that random returns an element from the list
        for _ in range(10):
            element = lst.random()
            self.assertIn(element, [1, 2, 3, 4, 5])
        
        # Test with custom Random instance
        rng = random.Random(42)
        element = lst.random(rng)
        self.assertIn(element, [1, 2, 3, 4, 5])
        
        # Test with empty list
        empty_lst = KotList()
        with self.assertRaises(IndexError) as cm:
            empty_lst.random()
        self.assertIn("List is empty", str(cm.exception))
    
    def test_random_or_null(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test that random_or_null returns an element from the list
        for _ in range(10):
            element = lst.random_or_null()
            self.assertIn(element, [1, 2, 3, 4, 5])
        
        # Test with custom Random instance
        rng = random.Random(42)
        element = lst.random_or_null(rng)
        self.assertIn(element, [1, 2, 3, 4, 5])
        
        # Test alias
        element = lst.random_or_none()
        self.assertIn(element, [1, 2, 3, 4, 5])
        
        # Test alias with custom Random instance
        element = lst.random_or_none(rng)
        self.assertIn(element, [1, 2, 3, 4, 5])
        
        # Test with empty list
        empty_lst = KotList()
        self.assertIsNone(empty_lst.random_or_null())
        self.assertIsNone(empty_lst.random_or_none())


class TestKotListSublistOps(unittest.TestCase):
    def test_slice(self):
        lst = KotList([10, 20, 30, 40, 50])
        
        # Test normal slice
        sliced = lst.slice([0, 2, 4])
        self.assertEqual(sliced.to_list(), [10, 30, 50])
        
        # Test with out of bounds index
        with self.assertRaises(IndexError):
            lst.slice([0, 2, 10])
        
        # Test empty indices
        empty_slice = lst.slice([])
        self.assertEqual(empty_slice.to_list(), [])
    
    def test_take(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test normal take
        self.assertEqual(lst.take(3).to_list(), [1, 2, 3])
        self.assertEqual(lst.take(0).to_list(), [])
        self.assertEqual(lst.take(10).to_list(), [1, 2, 3, 4, 5])
        
        # Test negative n
        with self.assertRaises(ValueError):
            lst.take(-1)
    
    def test_take_last(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test normal take_last
        self.assertEqual(lst.take_last(3).to_list(), [3, 4, 5])
        self.assertEqual(lst.take_last(0).to_list(), [])
        self.assertEqual(lst.take_last(10).to_list(), [1, 2, 3, 4, 5])
        
        # Test negative n
        with self.assertRaises(ValueError):
            lst.take_last(-1)
    
    def test_take_while(self):
        lst = KotList([1, 2, 3, 4, 5, 1, 2])
        
        # Test take_while
        self.assertEqual(lst.take_while(lambda x: x < 4).to_list(), [1, 2, 3])
        self.assertEqual(lst.take_while(lambda x: x < 1).to_list(), [])
        self.assertEqual(lst.take_while(lambda x: x < 10).to_list(), [1, 2, 3, 4, 5, 1, 2])
    
    def test_take_last_while(self):
        lst = KotList([1, 2, 3, 4, 5, 1, 2])
        
        # Test take_last_while
        self.assertEqual(lst.take_last_while(lambda x: x < 3).to_list(), [1, 2])
        self.assertEqual(lst.take_last_while(lambda x: x < 1).to_list(), [])
        self.assertEqual(lst.take_last_while(lambda x: x < 10).to_list(), [1, 2, 3, 4, 5, 1, 2])
    
    def test_drop(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test normal drop
        self.assertEqual(lst.drop(2).to_list(), [3, 4, 5])
        self.assertEqual(lst.drop(0).to_list(), [1, 2, 3, 4, 5])
        self.assertEqual(lst.drop(10).to_list(), [])
        
        # Test negative n
        with self.assertRaises(ValueError):
            lst.drop(-1)
    
    def test_drop_last(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test normal drop_last
        self.assertEqual(lst.drop_last(2).to_list(), [1, 2, 3])
        self.assertEqual(lst.drop_last(0).to_list(), [1, 2, 3, 4, 5])
        self.assertEqual(lst.drop_last(10).to_list(), [])
        
        # Test negative n
        with self.assertRaises(ValueError):
            lst.drop_last(-1)
    
    def test_drop_while(self):
        lst = KotList([1, 2, 3, 4, 5, 1, 2])
        
        # Test drop_while
        self.assertEqual(lst.drop_while(lambda x: x < 4).to_list(), [4, 5, 1, 2])
        self.assertEqual(lst.drop_while(lambda x: x < 1).to_list(), [1, 2, 3, 4, 5, 1, 2])
        self.assertEqual(lst.drop_while(lambda x: x < 10).to_list(), [])
    
    def test_drop_last_while(self):
        lst = KotList([1, 2, 3, 4, 5, 1, 2])
        
        # Test drop_last_while
        self.assertEqual(lst.drop_last_while(lambda x: x < 3).to_list(), [1, 2, 3, 4, 5])
        self.assertEqual(lst.drop_last_while(lambda x: x < 1).to_list(), [1, 2, 3, 4, 5, 1, 2])
        self.assertEqual(lst.drop_last_while(lambda x: x < 10).to_list(), [])


class TestKotListAdvancedTransform(unittest.TestCase):
    def test_map_indexed_not_null(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test map_indexed_not_null
        result = lst.map_indexed_not_null(lambda i, x: x * i if i % 2 == 0 else None)
        self.assertEqual(result.to_list(), [0, 6, 20])
        
        # Test alias
        result2 = lst.map_indexed_not_none(lambda i, x: x * i if i % 2 == 0 else None)
        self.assertEqual(result2.to_list(), [0, 6, 20])
    
    def test_flat_map_indexed(self):
        lst = KotList(['a', 'b', 'c'])
        
        # Test flat_map_indexed
        result = lst.flat_map_indexed(lambda i, x: [x, str(i)])
        self.assertEqual(result.to_list(), ['a', '0', 'b', '1', 'c', '2'])
    
    def test_zip_with_next(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test zip_with_next
        result = lst.zip_with_next()
        self.assertEqual(result.to_list(), [(1, 2), (2, 3), (3, 4), (4, 5)])
        
        # Test with single element
        single = KotList([1])
        self.assertEqual(single.zip_with_next().to_list(), [])
        
        # Test with empty list
        empty = KotList()
        self.assertEqual(empty.zip_with_next().to_list(), [])
    
    def test_zip_with_next_transform(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test zip_with_next_transform
        result = lst.zip_with_next_transform(lambda a, b: a + b)
        self.assertEqual(result.to_list(), [3, 5, 7, 9])
        
        # Test with single element
        single = KotList([1])
        self.assertEqual(single.zip_with_next_transform(lambda a, b: a + b).to_list(), [])


class TestKotListNewSearch(unittest.TestCase):
    def test_find(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test find (alias for first_or_null_predicate)
        self.assertEqual(lst.find(lambda x: x > 3), 4)
        self.assertIsNone(lst.find(lambda x: x > 10))
    
    def test_find_last(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test find_last (alias for last_or_null_predicate)
        self.assertEqual(lst.find_last(lambda x: x > 3), 5)
        self.assertIsNone(lst.find_last(lambda x: x > 10))
    
    def test_first_not_null_of(self):
        lst = KotList(['hello', '', 'world', ''])
        
        # Test first_not_null_of
        result = lst.first_not_null_of(lambda x: x.upper() if x else None)
        self.assertEqual(result, 'HELLO')
        
        # Test alias
        result2 = lst.first_not_none_of(lambda x: x.upper() if x else None)
        self.assertEqual(result2, 'HELLO')
        
        # Test with no non-null results
        with self.assertRaises(ValueError):
            lst.first_not_null_of(lambda x: None)
    
    def test_first_not_null_of_or_null(self):
        lst = KotList(['', '', ''])
        
        # Test first_not_null_of_or_null
        result = lst.first_not_null_of_or_null(lambda x: x.upper() if x else None)
        self.assertIsNone(result)
        
        # Test alias
        result2 = lst.first_not_none_of_or_none(lambda x: x.upper() if x else None)
        self.assertIsNone(result2)
        
        # Test with some non-null results
        lst2 = KotList(['', 'hello', 'world'])
        result3 = lst2.first_not_null_of_or_null(lambda x: x.upper() if x else None)
        self.assertEqual(result3, 'HELLO')


class TestKotListAdvancedAggregation(unittest.TestCase):
    def test_max_by(self):
        lst = KotList(['a', 'bbb', 'cc'])
        
        # Test max_by
        result = lst.max_by(len)
        self.assertEqual(result, 'bbb')
        
        # Test with empty list
        empty = KotList()
        with self.assertRaises(ValueError):
            empty.max_by(len)
    
    def test_min_by(self):
        lst = KotList(['a', 'bbb', 'cc'])
        
        # Test min_by
        result = lst.min_by(len)
        self.assertEqual(result, 'a')
        
        # Test with empty list
        empty = KotList()
        with self.assertRaises(ValueError):
            empty.min_by(len)
    
    def test_max_of(self):
        lst = KotList(['a', 'bbb', 'cc'])
        
        # Test max_of
        result = lst.max_of(len)
        self.assertEqual(result, 3)
        
        # Test with empty list
        empty = KotList()
        with self.assertRaises(ValueError):
            empty.max_of(len)
    
    def test_min_of(self):
        lst = KotList(['a', 'bbb', 'cc'])
        
        # Test min_of
        result = lst.min_of(len)
        self.assertEqual(result, 1)
        
        # Test with empty list
        empty = KotList()
        with self.assertRaises(ValueError):
            empty.min_of(len)
    
    def test_max_of_or_null(self):
        lst = KotList(['a', 'bbb', 'cc'])
        
        # Test max_of_or_null
        result = lst.max_of_or_null(len)
        self.assertEqual(result, 3)
        
        # Test alias
        result2 = lst.max_of_or_none(len)
        self.assertEqual(result2, 3)
        
        # Test with empty list
        empty = KotList()
        self.assertIsNone(empty.max_of_or_null(len))
        self.assertIsNone(empty.max_of_or_none(len))
    
    def test_min_of_or_null(self):
        lst = KotList(['a', 'bbb', 'cc'])
        
        # Test min_of_or_null
        result = lst.min_of_or_null(len)
        self.assertEqual(result, 1)
        
        # Test alias
        result2 = lst.min_of_or_none(len)
        self.assertEqual(result2, 1)
        
        # Test with empty list
        empty = KotList()
        self.assertIsNone(empty.min_of_or_null(len))
        self.assertIsNone(empty.min_of_or_none(len))
    
    def test_max_of_with(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test max_of_with with custom comparator
        def reverse_comparator(a, b):
            return b - a  # Reverse order
        
        result = lst.max_of_with_or_null(reverse_comparator, lambda x: x)
        self.assertEqual(result, 1)  # Minimum in normal order
        
        # Test alias
        result2 = lst.max_of_with_or_none(reverse_comparator, lambda x: x)
        self.assertEqual(result2, 1)
        
        # Test max_of_with (non-null version) with empty list
        empty = KotList()
        with self.assertRaises(ValueError) as cm:
            empty.max_of_with(reverse_comparator, lambda x: x)
        self.assertIn("Cannot find max of empty list", str(cm.exception))
        
        # Test max_of_with with non-empty list
        result3 = lst.max_of_with(reverse_comparator, lambda x: x * 2)
        self.assertEqual(result3, 2)  # 1 * 2 = 2 (minimum * 2)
        
        # Test max_of_with where multiple comparisons update the result
        # Normal comparator to test the loop properly
        def normal_comparator(a, b):
            return a - b
        
        result4 = lst.max_of_with(normal_comparator, lambda x: x)
        self.assertEqual(result4, 5)  # Maximum value
        
        # Test with more complex data
        strings = KotList(['a', 'bb', 'ccc', 'dd', 'e'])
        result5 = strings.max_of_with(lambda a, b: len(a) - len(b), lambda x: x)
        self.assertEqual(result5, 'ccc')  # Longest string
        
        # Test max_of_with_or_null with empty list  
        self.assertIsNone(empty.max_of_with_or_null(reverse_comparator, lambda x: x))
        
        # Test with list where loop iterates through all values
        lst6 = KotList([3, 1, 4, 1, 5, 9, 2, 6, 5])
        result6 = lst6.max_of_with_or_null(normal_comparator, lambda x: x)
        self.assertEqual(result6, 9)
    
    def test_min_of_with(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test min_of_with with custom comparator
        def reverse_comparator(a, b):
            return b - a  # Reverse order
        
        result = lst.min_of_with_or_null(reverse_comparator, lambda x: x)
        self.assertEqual(result, 5)  # Maximum in normal order
        
        # Test alias
        result2 = lst.min_of_with_or_none(reverse_comparator, lambda x: x)
        self.assertEqual(result2, 5)
        
        # Test min_of_with (non-null version) with empty list
        empty = KotList()
        with self.assertRaises(ValueError) as cm:
            empty.min_of_with(reverse_comparator, lambda x: x)
        self.assertIn("Cannot find min of empty list", str(cm.exception))
        
        # Test min_of_with with non-empty list
        result3 = lst.min_of_with(reverse_comparator, lambda x: x * 2)
        self.assertEqual(result3, 10)  # 5 * 2 = 10 (maximum * 2)
        
        # Test min_of_with where multiple comparisons update the result
        # Normal comparator to test the loop properly
        def normal_comparator(a, b):
            return a - b
        
        result4 = lst.min_of_with(normal_comparator, lambda x: x)
        self.assertEqual(result4, 1)  # Minimum value
        
        # Test with more complex data
        strings = KotList(['aaa', 'bb', 'c', 'dd', 'eee'])
        result5 = strings.min_of_with(lambda a, b: len(a) - len(b), lambda x: x)
        self.assertEqual(result5, 'c')  # Shortest string
        
        # Test min_of_with_or_null with empty list
        self.assertIsNone(empty.min_of_with_or_null(reverse_comparator, lambda x: x))
        
        # Test with list where loop iterates through all values
        lst6 = KotList([3, 8, 4, 8, 5, 1, 2, 6, 5])
        result6 = lst6.min_of_with_or_null(normal_comparator, lambda x: x)
        self.assertEqual(result6, 1)


class TestKotListAdvancedFoldReduce(unittest.TestCase):
    def test_fold_indexed(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test fold_indexed
        result = lst.fold_indexed(0, lambda i, acc, x: acc + x * i)
        self.assertEqual(result, 0 + 0*1 + 1*2 + 2*3 + 3*4 + 4*5)  # 0 + 0 + 2 + 6 + 12 + 20 = 40
    
    def test_fold_right(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test fold_right
        result = lst.fold_right('', lambda x, acc: str(x) + acc)
        self.assertEqual(result, '12345')
    
    def test_fold_right_indexed(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test fold_right_indexed
        result = lst.fold_right_indexed(0, lambda i, x, acc: acc + x * i)
        self.assertEqual(result, 4*5 + 3*4 + 2*3 + 1*2 + 0*1)  # 20 + 12 + 6 + 2 + 0 = 40
    
    def test_reduce_indexed(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test reduce_indexed
        result = lst.reduce_indexed(lambda i, acc, x: acc + x * i)
        self.assertEqual(result, 1 + 2*1 + 3*2 + 4*3 + 5*4)  # 1 + 2 + 6 + 12 + 20 = 41
        
        # Test with empty list
        empty = KotList()
        with self.assertRaises(ValueError):
            empty.reduce_indexed(lambda i, acc, x: acc + x)
    
    def test_reduce_right(self):
        lst = KotList(['a', 'b', 'c', 'd'])
        
        # Test reduce_right
        result = lst.reduce_right(lambda x, acc: x + acc)
        self.assertEqual(result, 'abcd')
        
        # Test with empty list
        empty = KotList()
        with self.assertRaises(ValueError) as cm:
            empty.reduce_right(lambda x, acc: x + acc)
        self.assertIn("Cannot reduce empty list", str(cm.exception))
    
    def test_reduce_right_indexed(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test reduce_right_indexed
        result = lst.reduce_right_indexed(lambda i, x, acc: x * i + acc)
        self.assertEqual(result, 0*1 + 1*2 + 2*3 + 3*4 + 5)  # 0 + 2 + 6 + 12 + 5 = 25
        
        # Test with empty list
        empty = KotList()
        with self.assertRaises(ValueError) as cm:
            empty.reduce_right_indexed(lambda i, x, acc: x + acc)
        self.assertIn("Cannot reduce empty list", str(cm.exception))
    
    def test_reduce_variations_or_null(self):
        lst = KotList([1, 2, 3])
        empty = KotList()
        
        # Test reduce_or_null
        self.assertEqual(lst.reduce_or_null(lambda a, b: a + b), 6)
        self.assertIsNone(empty.reduce_or_null(lambda a, b: a + b))
        self.assertIsNone(empty.reduce_or_none(lambda a, b: a + b))  # alias
        
        # Test reduce_indexed_or_null
        self.assertEqual(lst.reduce_indexed_or_null(lambda i, a, b: a + b * i), 1 + 2*1 + 3*2)
        self.assertIsNone(empty.reduce_indexed_or_null(lambda i, a, b: a + b))
        self.assertIsNone(empty.reduce_indexed_or_none(lambda i, a, b: a + b))  # alias
        
        # Test reduce_right_or_null
        self.assertEqual(lst.reduce_right_or_null(lambda a, b: str(a) + str(b)), '123')
        self.assertIsNone(empty.reduce_right_or_null(lambda a, b: a + b))
        self.assertIsNone(empty.reduce_right_or_none(lambda a, b: a + b))  # alias
        
        # Test reduce_right_indexed_or_null
        self.assertEqual(lst.reduce_right_indexed_or_null(lambda i, a, b: a * i + b), 0*1 + 1*2 + 3)
        self.assertIsNone(empty.reduce_right_indexed_or_null(lambda i, a, b: a + b))
        self.assertIsNone(empty.reduce_right_indexed_or_none(lambda i, a, b: a + b))  # alias
    
    def test_running_fold(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test running_fold (should be same as scan)
        result = lst.running_fold(0, lambda acc, x: acc + x)
        self.assertEqual(result.to_list(), [0, 1, 3, 6, 10, 15])
    
    def test_running_fold_indexed(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test running_fold_indexed
        result = lst.running_fold_indexed(0, lambda i, acc, x: acc + x * i)
        self.assertEqual(result.to_list(), [0, 0, 2, 8, 20, 40])
    
    def test_scan_indexed(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test scan_indexed (alias for running_fold_indexed)
        result = lst.scan_indexed(0, lambda i, acc, x: acc + x * i)
        self.assertEqual(result.to_list(), [0, 0, 2, 8, 20, 40])
    
    def test_running_reduce(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test running_reduce
        result = lst.running_reduce(lambda acc, x: acc + x)
        self.assertEqual(result.to_list(), [1, 3, 6, 10, 15])
        
        # Test with empty list
        empty = KotList()
        self.assertEqual(empty.running_reduce(lambda a, b: a + b).to_list(), [])
    
    def test_running_reduce_indexed(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test running_reduce_indexed
        result = lst.running_reduce_indexed(lambda i, acc, x: acc + x * i)
        self.assertEqual(result.to_list(), [1, 3, 9, 21, 41])
        
        # Test with empty list
        empty = KotList()
        self.assertEqual(empty.running_reduce_indexed(lambda i, acc, x: acc + x).to_list(), [])


class TestKotListOtherMethods(unittest.TestCase):
    def test_as_reversed(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test as_reversed
        reversed_lst = lst.as_reversed()
        self.assertEqual(reversed_lst.to_list(), [5, 4, 3, 2, 1])
    
    def test_as_sequence(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test as_sequence
        seq = lst.as_sequence()
        self.assertEqual(list(seq), [1, 2, 3, 4, 5])
    
    def test_with_index(self):
        lst = KotList(['a', 'b', 'c'])
        
        # Test with_index
        indexed = list(lst.with_index())
        self.assertEqual(indexed, [(0, 'a'), (1, 'b'), (2, 'c')])
    
    def test_on_each_indexed(self):
        lst = KotList([1, 2, 3])
        
        # Test on_each_indexed
        results = []
        returned = lst.on_each_indexed(lambda i, x: results.append((i, x)))
        self.assertEqual(results, [(0, 1), (1, 2), (2, 3)])
        self.assertIs(returned, lst)  # Should return self
    
    def test_if_empty(self):
        # Test with non-empty list
        lst = KotList([1, 2, 3])
        result = lst.if_empty(lambda: KotList([4, 5, 6]))
        self.assertEqual(result.to_list(), [1, 2, 3])
        
        # Test with empty list
        empty = KotList()
        result = empty.if_empty(lambda: KotList([4, 5, 6]))
        self.assertEqual(result.to_list(), [4, 5, 6])
    
    def test_list_iterator(self):
        lst = KotList([1, 2, 3, 4, 5])
        
        # Test list_iterator from beginning
        it = lst.list_iterator()
        self.assertEqual(list(it), [1, 2, 3, 4, 5])
        
        # Test list_iterator from index
        it = lst.list_iterator(2)
        self.assertEqual(list(it), [3, 4, 5])
        
        # Test with invalid index
        with self.assertRaises(IndexError):
            lst.list_iterator(-1)
        with self.assertRaises(IndexError):
            lst.list_iterator(6)
    
    def test_operator_overloads(self):
        lst1 = KotList([1, 2, 3])
        lst2 = KotList([4, 5])
        
        # Test + operator
        result = lst1 + 4
        self.assertEqual(result.to_list(), [1, 2, 3, 4])
        
        result = lst1 + [4, 5]
        self.assertEqual(result.to_list(), [1, 2, 3, 4, 5])
        
        # Test - operator
        lst3 = KotList([1, 2, 3, 2, 4])
        result = lst3 - 2
        self.assertEqual(result.to_list(), [1, 3, 2, 4])  # Only first occurrence removed
        
        result = lst3 - [2, 4]
        self.assertEqual(result.to_list(), [1, 3, 2])  # Kotlin-compatible: first occurrence of each element removed


class TestKotListTypeSpecification(unittest.TestCase):
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
        
        # Test creating typed KotList with parent type
        animals = KotList[Animal]()
        self.assertEqual(len(animals), 0)
        
        # Convert to mutable and add different subclass instances
        mutable_animals = animals.to_kot_mutable_list()
        mutable_animals.add(Dog("Buddy"))
        mutable_animals.add(Cat("Whiskers"))
        self.assertEqual(len(mutable_animals), 2)
        
        # Test with initial elements
        animals2 = KotList[Animal]([Dog("Max"), Cat("Luna")])
        self.assertEqual(len(animals2), 2)
        self.assertIsInstance(animals2[0], Dog)
        self.assertIsInstance(animals2[1], Cat)
    
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
        
        # Test creating empty typed KotList
        animals = KotList.of_type(Animal)
        self.assertEqual(len(animals), 0)
        
        # Convert to mutable and add different subclass instances
        mutable_animals = animals.to_kot_mutable_list()
        mutable_animals.add(Dog("Buddy"))
        mutable_animals.add(Cat("Whiskers"))
        self.assertEqual(len(mutable_animals), 2)
        
        # Test with initial elements
        animals2 = KotList.of_type(Animal, [Dog("Max"), Cat("Luna")])
        self.assertEqual(len(animals2), 2)
        self.assertIsInstance(animals2[0], Dog)
        self.assertIsInstance(animals2[1], Cat)
        
        # Test type checking is enforced
        class NotAnimal:
            pass
        
        mutable_animals2 = animals2.to_kot_mutable_list()
        with self.assertRaises(TypeError):
            mutable_animals2.add(NotAnimal())
    
    def test_type_preservation_in_conversions(self):
        """Test that type information is preserved during conversions"""
        # Define test classes with inheritance
        class Animal:
            def __init__(self, name):
                self.name = name
        
        class Dog(Animal):
            pass
        
        # Test KotList type preservation
        animals = KotList.of_type(Animal, [Dog("Buddy")])
        self.assertEqual(animals._element_type, Animal)
        
        # Test to_kot_list preserves type
        copied = animals.to_kot_list()
        self.assertEqual(copied._element_type, Animal)
        
        # Test to_kot_mutable_list preserves type
        mutable = animals.to_kot_mutable_list()
        self.assertEqual(mutable._element_type, Animal)
        # Verify we can still add correct types
        mutable.add(Dog("Max"))
        self.assertEqual(len(mutable), 2)
        
        # Test to_kot_set preserves type
        kot_set = animals.to_kot_set()
        self.assertEqual(kot_set._element_type, Animal)
        
        # Test to_kot_mutable_set preserves type
        mutable_set = animals.to_kot_mutable_set()
        self.assertEqual(mutable_set._element_type, Animal)
        # Verify we can still add correct types
        mutable_set.add(Dog("Rex"))
        self.assertEqual(mutable_set.size, 2)
    
    def test_kot_list_element_type_with_class_getitem(self):
        """Test KotList with KotList[T] as element type using __class_getitem__ syntax"""
        from kotcollections import KotMutableList
        
        # Define test classes
        class Task:
            def __init__(self, name):
                self.name = name
                
        # Create a list with KotList[Task] as element type using __class_getitem__ syntax
        lists_of_lists = KotMutableList[KotList[Task]]()
        
        # Create a mutable list with Task type
        tasks1 = KotMutableList[Task]()
        tasks1.add(Task("Buy milk"))
        tasks1.add(Task("Walk dog"))
        
        # Convert to immutable KotList
        immutable_tasks1 = tasks1.to_kot_list()
        
        # This should work without TypeError
        lists_of_lists.add(immutable_tasks1)
        
        # Create another task list
        tasks2 = KotMutableList[Task]()
        tasks2.add(Task("Write code"))
        
        # Convert to immutable KotList
        immutable_tasks2 = tasks2.to_kot_list()
        lists_of_lists.add(immutable_tasks2)
        
        # Verify the elements were stored correctly
        self.assertEqual(lists_of_lists.size, 2)
        self.assertEqual(lists_of_lists[0][0].name, "Buy milk")
        self.assertEqual(lists_of_lists[1][0].name, "Write code")
    
    def test_class_getitem_and_of_type_same_type(self):
        """Test that KotList[T]() and KotList.of_type(T) return functionally equivalent types"""
        from kotcollections import KotMutableList
        
        # Define test class
        class Animal:
            def __init__(self, name):
                self.name = name
        
        # Create instances using both methods
        list1 = KotList[Animal]()
        list2 = KotList.of_type(Animal, [])
        
        # Without cache, they won't be the exact same type object, but functionally equivalent
        self.assertEqual(type(list1).__name__, type(list2).__name__)
        self.assertEqual(type(list1).__name__, "KotList[Animal]")
        
        # Both should have the same element type
        self.assertEqual(list1._element_type, Animal)
        self.assertEqual(list2._element_type, Animal)
        
        # Test with KotMutableList too
        mlist1 = KotMutableList[Animal]()
        mlist2 = KotMutableList.of_type(Animal, [])
        
        # Without cache, they won't be the exact same type object, but functionally equivalent
        self.assertEqual(type(mlist1).__name__, type(mlist2).__name__)
        self.assertEqual(type(mlist1).__name__, "KotMutableList[Animal]")


class TestKotListNewAPIs(unittest.TestCase):
    """Test newly implemented APIs"""
    
    def test_subtract(self):
        """Test subtract method (returns KotSet)"""
        lst1 = KotList([1, 2, 3, 4, 5])
        lst2 = [2, 4]
        result = lst1.subtract(lst2)
        from kotcollections import KotSet
        self.assertIsInstance(result, KotSet)
        self.assertEqual(set(result.to_list()), {1, 3, 5})
        
        # Test with empty list
        empty = KotList()
        result_empty = empty.subtract([1, 2])
        self.assertEqual(result_empty.to_list(), [])
        
        # Test with KotSet
        kot_set = KotSet([2, 4, 6])
        result_set = lst1.subtract(kot_set)
        self.assertEqual(result_set.to_list(), [1, 3, 5])
        
        # Test with KotMap values
        kot_map = KotMap({"a": 2, "b": 4})
        result_map = lst1.subtract(kot_map)
        self.assertEqual(result_map.to_list(), [1, 3, 5])
    
    def test_slice_range(self):
        """Test slice_range method"""
        lst = KotList([10, 20, 30, 40, 50])
        
        # Test basic range
        result = lst.slice_range(range(1, 4))
        self.assertEqual(result.to_list(), [20, 30, 40])
        
        # Test with step
        result_step = lst.slice_range(range(0, 5, 2))
        self.assertEqual(result_step.to_list(), [10, 30, 50])
        
        # Test empty range
        result_empty = lst.slice_range(range(0, 0))
        self.assertEqual(result_empty.to_list(), [])
        
        # Test out of bounds should raise error
        with self.assertRaises(IndexError):
            lst.slice_range(range(0, 10))


class TestKotListAssociate(unittest.TestCase):
    def test_associate_basic(self):
        """Test associate() creates correct key-value pairs."""
        lst = KotList(["apple", "banana", "cherry"])
        result = lst.associate(lambda s: (s[0], len(s)))
        self.assertEqual(result.size, 3)
        self.assertEqual(result.get('a'), 5)
        self.assertEqual(result.get('b'), 6)
        self.assertEqual(result.get('c'), 6)

    def test_associate_with_duplicates(self):
        """Test associate() with duplicate keys - last one wins."""
        lst = KotList(["apple", "apricot", "banana"])
        result = lst.associate(lambda s: (s[0], s))
        self.assertEqual(result.size, 2)  # 'a' and 'b'
        self.assertEqual(result.get('a'), 'apricot')  # last 'a' word wins
        self.assertEqual(result.get('b'), 'banana')

    def test_associate_empty_list(self):
        """Test associate() on empty list."""
        lst = KotList([])
        result = lst.associate(lambda x: (x, x))
        self.assertEqual(result.size, 0)
        self.assertTrue(result.is_empty())

    def test_associate_number_pairs(self):
        """Test associate() with numeric transformations."""
        lst = KotList([1, 2, 3, 4, 5])
        result = lst.associate(lambda x: (x, x * x))
        self.assertEqual(result.size, 5)
        self.assertEqual(result.get(3), 9)
        self.assertEqual(result.get(5), 25)

    def test_associate_returns_kot_map(self):
        """Test associate() returns KotMap instance."""
        lst = KotList([1, 2, 3])
        result = lst.associate(lambda x: (x, str(x)))
        self.assertIsInstance(result, KotMap)


class TestKotListMaxMin(unittest.TestCase):
    def test_max_basic(self):
        """Test max() returns largest element."""
        lst = KotList([1, 5, 3, 9, 2])
        self.assertEqual(lst.max(), 9)

    def test_max_single_element(self):
        """Test max() with single element."""
        lst = KotList([42])
        self.assertEqual(lst.max(), 42)

    def test_max_negative_numbers(self):
        """Test max() with negative numbers."""
        lst = KotList([-5, -1, -10, -3])
        self.assertEqual(lst.max(), -1)

    def test_max_strings(self):
        """Test max() with strings."""
        lst = KotList(["apple", "banana", "cherry", "date"])
        self.assertEqual(lst.max(), "date")

    def test_max_empty_list_raises_error(self):
        """Test max() raises ValueError on empty list."""
        lst = KotList([])
        with self.assertRaises(ValueError) as cm:
            lst.max()
        self.assertEqual(str(cm.exception), "List is empty")

    def test_min_basic(self):
        """Test min() returns smallest element."""
        lst = KotList([1, 5, 3, 9, 2])
        self.assertEqual(lst.min(), 1)

    def test_min_single_element(self):
        """Test min() with single element."""
        lst = KotList([42])
        self.assertEqual(lst.min(), 42)

    def test_min_negative_numbers(self):
        """Test min() with negative numbers."""
        lst = KotList([-5, -1, -10, -3])
        self.assertEqual(lst.min(), -10)

    def test_min_strings(self):
        """Test min() with strings."""
        lst = KotList(["apple", "banana", "cherry", "date"])
        self.assertEqual(lst.min(), "apple")

    def test_min_empty_list_raises_error(self):
        """Test min() raises ValueError on empty list."""
        lst = KotList([])
        with self.assertRaises(ValueError) as cm:
            lst.min()
        self.assertEqual(str(cm.exception), "List is empty")

    def test_max_or_none_alias(self):
        """Test max_or_none() alias works correctly."""
        lst = KotList([1, 5, 3])
        self.assertEqual(lst.max_or_none(), 5)
        self.assertEqual(lst.max_or_none(), lst.max_or_null())

        empty = KotList([])
        self.assertIsNone(empty.max_or_none())
        self.assertEqual(empty.max_or_none(), empty.max_or_null())

    def test_min_or_none_alias(self):
        """Test min_or_none() alias works correctly."""
        lst = KotList([1, 5, 3])
        self.assertEqual(lst.min_or_none(), 1)
        self.assertEqual(lst.min_or_none(), lst.min_or_null())

        empty = KotList([])
        self.assertIsNone(empty.min_or_none())
        self.assertEqual(empty.min_or_none(), empty.min_or_null())
