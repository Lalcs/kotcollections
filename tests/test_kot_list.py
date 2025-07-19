import random
import unittest

from kotcollections import KotList


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

    def test_index_of(self):
        lst = KotList([1, 2, 3, 2, 5])
        self.assertEqual(lst.index_of(2), 1)
        self.assertEqual(lst.index_of(5), 4)
        self.assertEqual(lst.index_of(6), -1)

    def test_last_index_of(self):
        lst = KotList([1, 2, 3, 2, 5])
        self.assertEqual(lst.last_index_of(2), 3)
        self.assertEqual(lst.last_index_of(1), 0)
        self.assertEqual(lst.last_index_of(6), -1)

    def test_index_of_first(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.index_of_first(lambda x: x > 3), 3)
        self.assertEqual(lst.index_of_first(lambda x: x > 10), -1)

    def test_index_of_last(self):
        lst = KotList([1, 2, 3, 4, 5])
        self.assertEqual(lst.index_of_last(lambda x: x < 4), 2)
        self.assertEqual(lst.index_of_last(lambda x: x > 10), -1)

    def test_binary_search_default(self):
        lst = KotList([1, 3, 5, 7, 9])
        self.assertEqual(lst.binary_search(5), 2)
        self.assertEqual(lst.binary_search(1), 0)
        self.assertEqual(lst.binary_search(9), 4)

        # Not found cases
        self.assertEqual(lst.binary_search(0), -1)
        self.assertEqual(lst.binary_search(4), -3)
        self.assertEqual(lst.binary_search(10), -6)

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
        self.assertEqual(assoc, {'a': 1, 'bb': 2, 'ccc': 3})

    def test_associate_by(self):
        lst = KotList(['a', 'bb', 'ccc'])
        assoc = lst.associate_by(lambda x: len(x))
        self.assertEqual(assoc, {1: 'a', 2: 'bb', 3: 'ccc'})

    def test_associate_by_with_value(self):
        lst = KotList(['a', 'bb', 'ccc'])
        assoc = lst.associate_by_with_value(lambda x: len(x), lambda x: x.upper())
        self.assertEqual(assoc, {1: 'A', 2: 'BB', 3: 'CCC'})


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
        with self.assertRaises(ValueError):
            empty_lst.average()


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
        self.assertEqual(grouped[0].to_list(), [2, 4, 6])
        self.assertEqual(grouped[1].to_list(), [1, 3, 5])

    def test_group_by_with_value(self):
        lst = KotList(['a', 'bb', 'ccc', 'dd', 'e'])
        grouped = lst.group_by_with_value(lambda x: len(x), lambda x: x.upper())
        self.assertEqual(grouped[1].to_list(), ['A', 'E'])
        self.assertEqual(grouped[2].to_list(), ['BB', 'DD'])
        self.assertEqual(grouped[3].to_list(), ['CCC'])

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
        self.assertEqual(intersection.to_list(), [3, 4, 5])

    def test_union(self):
        lst1 = KotList([1, 2, 3])
        lst2 = [3, 4, 5]
        union = lst1.union(lst2)
        self.assertEqual(union.to_list(), [1, 2, 3, 4, 5])

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
        mutable = lst.to_mutable_list()
        self.assertIsInstance(mutable, KotMutableList)
        self.assertEqual(mutable.to_list(), [1, 2, 3])

    def test_to_set(self):
        lst = KotList([1, 2, 2, 3, 3, 3])
        python_set = lst.to_set()
        self.assertEqual(python_set, {1, 2, 3})
        self.assertIsInstance(python_set, set)

    def test_to_mutable_set(self):
        lst = KotList([1, 2, 2, 3, 3, 3])
        python_set = lst.to_mutable_set()
        self.assertEqual(python_set, {1, 2, 3})
        self.assertIsInstance(python_set, set)


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
        self.assertIn("Cannot add KotList to KotList[int]", str(cm.exception))
    
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
