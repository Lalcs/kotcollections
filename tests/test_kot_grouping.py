import unittest

from kotcollections import KotList, KotMap, KotGrouping


class TestKotGroupingBasics(unittest.TestCase):
    def test_grouping_creation(self):
        """Test Grouping can be created from KotList."""
        lst = KotList(["apple", "apricot", "banana"])
        grouping = lst.grouping_by(lambda s: s[0])
        self.assertIsInstance(grouping, KotGrouping)


class TestKotGroupingEachCount(unittest.TestCase):
    def test_each_count_basic(self):
        """Test each_count() counts elements in each group."""
        lst = KotList(["apple", "apricot", "banana", "cherry", "avocado"])
        grouping = lst.grouping_by(lambda s: s[0])
        result = grouping.each_count()

        self.assertIsInstance(result, KotMap)
        self.assertEqual(result.get('a'), 3)
        self.assertEqual(result.get('b'), 1)
        self.assertEqual(result.get('c'), 1)

    def test_each_count_with_numbers(self):
        """Test each_count() with numeric grouping."""
        lst = KotList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        grouping = lst.grouping_by(lambda x: x % 3)
        result = grouping.each_count()

        self.assertEqual(result.get(0), 3)  # 3, 6, 9
        self.assertEqual(result.get(1), 4)  # 1, 4, 7, 10
        self.assertEqual(result.get(2), 3)  # 2, 5, 8

    def test_each_count_empty_list(self):
        """Test each_count() on empty list."""
        lst = KotList([])
        grouping = lst.grouping_by(lambda x: x)
        result = grouping.each_count()

        self.assertEqual(result.size, 0)
        self.assertTrue(result.is_empty())


class TestKotGroupingFold(unittest.TestCase):
    def test_fold_sum(self):
        """Test fold() with sum operation."""
        lst = KotList([1, 2, 3, 4, 5, 6])
        grouping = lst.grouping_by(lambda x: x % 2)
        result = grouping.fold(
            lambda k, e: 0,
            lambda k, acc, e: acc + e
        )

        self.assertEqual(result.get(0), 12)  # 2 + 4 + 6
        self.assertEqual(result.get(1), 9)  # 1 + 3 + 5

    def test_fold_concatenate_strings(self):
        """Test fold() with string concatenation."""
        lst = KotList(["apple", "apricot", "banana", "berry"])
        grouping = lst.grouping_by(lambda s: s[0])
        result = grouping.fold(
            lambda k, e: "",
            lambda k, acc, e: acc + e if acc == "" else acc + "," + e
        )

        self.assertEqual(result.get('a'), "apple,apricot")
        self.assertEqual(result.get('b'), "banana,berry")

    def test_fold_with_initial_value(self):
        """Test fold() with different initial values per group."""
        lst = KotList([1, 2, 3, 4, 5])
        grouping = lst.grouping_by(lambda x: x % 2)
        result = grouping.fold(
            lambda k, e: 10 if k == 0 else 100,  # Different initial values
            lambda k, acc, e: acc + e
        )

        # Even: 10 + 2 + 4 = 16
        self.assertEqual(result.get(0), 16)
        # Odd: 100 + 1 + 3 + 5 = 109
        self.assertEqual(result.get(1), 109)


class TestKotGroupingReduce(unittest.TestCase):
    def test_reduce_sum(self):
        """Test reduce() with sum operation."""
        lst = KotList([1, 2, 3, 4, 5, 6])
        grouping = lst.grouping_by(lambda x: x % 2)
        result = grouping.reduce(lambda k, acc, e: acc + e)

        self.assertEqual(result.get(0), 12)  # 2 + 4 + 6
        self.assertEqual(result.get(1), 9)  # 1 + 3 + 5

    def test_reduce_multiply(self):
        """Test reduce() with multiplication."""
        lst = KotList([1, 2, 3, 4, 5, 6])
        grouping = lst.grouping_by(lambda x: x % 2)
        result = grouping.reduce(lambda k, acc, e: acc * e)

        self.assertEqual(result.get(0), 48)  # 2 * 4 * 6
        self.assertEqual(result.get(1), 15)  # 1 * 3 * 5

    def test_reduce_single_element_groups(self):
        """Test reduce() with groups containing single element."""
        lst = KotList([1, 2, 3])
        grouping = lst.grouping_by(lambda x: x)  # Each element is its own group
        result = grouping.reduce(lambda k, acc, e: acc + e)

        self.assertEqual(result.get(1), 1)
        self.assertEqual(result.get(2), 2)
        self.assertEqual(result.get(3), 3)

    def test_reduce_strings(self):
        """Test reduce() with string concatenation."""
        lst = KotList(["apple", "apricot", "avocado", "banana"])
        grouping = lst.grouping_by(lambda s: s[0])
        result = grouping.reduce(lambda k, acc, e: acc + "," + e)

        self.assertEqual(result.get('a'), "apple,apricot,avocado")
        self.assertEqual(result.get('b'), "banana")


class TestKotGroupingAggregate(unittest.TestCase):
    def test_aggregate_with_first_flag(self):
        """Test aggregate() using the first flag."""
        lst = KotList(["apple", "apricot", "banana"])
        grouping = lst.grouping_by(lambda s: s[0])
        result = grouping.aggregate(
            lambda k, acc, e, first: e if first else acc + "," + e
        )

        self.assertEqual(result.get('a'), "apple,apricot")
        self.assertEqual(result.get('b'), "banana")

    def test_aggregate_sum(self):
        """Test aggregate() with sum operation."""
        lst = KotList([1, 2, 3, 4, 5, 6])
        grouping = lst.grouping_by(lambda x: x % 2)
        result = grouping.aggregate(
            lambda k, acc, e, first: e if first else acc + e
        )

        self.assertEqual(result.get(0), 12)  # 2 + 4 + 6
        self.assertEqual(result.get(1), 9)  # 1 + 3 + 5

    def test_aggregate_max_per_group(self):
        """Test aggregate() to find max in each group."""
        lst = KotList([1, 5, 2, 8, 3, 7, 4, 6])
        grouping = lst.grouping_by(lambda x: x % 3)
        result = grouping.aggregate(
            lambda k, acc, e, first: e if first else max(acc, e)
        )

        self.assertEqual(result.get(0), 6)  # max(3, 6)
        self.assertEqual(result.get(1), 7)  # max(1, 4, 7)
        self.assertEqual(result.get(2), 8)  # max(2, 5, 8)

    def test_aggregate_count_manually(self):
        """Test aggregate() to manually count elements."""
        lst = KotList(['a', 'b', 'a', 'c', 'a', 'b'])
        grouping = lst.grouping_by(lambda x: x)
        result = grouping.aggregate(
            lambda k, acc, e, first: 1 if first else acc + 1
        )

        self.assertEqual(result.get('a'), 3)
        self.assertEqual(result.get('b'), 2)
        self.assertEqual(result.get('c'), 1)

    def test_aggregate_with_none_accumulator(self):
        """Test aggregate() properly handles None accumulator for first element."""
        lst = KotList([10, 20, 30])
        grouping = lst.grouping_by(lambda x: x // 10)
        result = grouping.aggregate(
            lambda k, acc, e, first: e if acc is None else acc + e
        )

        self.assertEqual(result.get(1), 10)
        self.assertEqual(result.get(2), 20)
        self.assertEqual(result.get(3), 30)


class TestKotGroupingIntegration(unittest.TestCase):
    def test_group_by_vs_grouping_by(self):
        """Test difference between group_by() and grouping_by()."""
        lst = KotList([1, 2, 3, 4, 5, 6])

        # group_by() returns Map<K, List<V>>
        grouped = lst.group_by(lambda x: x % 2)
        self.assertIsInstance(grouped, KotMap)
        self.assertIsInstance(grouped.get(0), KotList)
        self.assertEqual(grouped.get(0).to_list(), [2, 4, 6])

        # grouping_by() returns KotGrouping<T, K>
        grouping = lst.grouping_by(lambda x: x % 2)
        self.assertIsInstance(grouping, KotGrouping)
        counts = grouping.each_count()
        self.assertEqual(counts.get(0), 3)

    def test_complex_grouping_scenario(self):
        """Test complex real-world grouping scenario."""
        # Group words by length, then count characters
        words = KotList(["cat", "dog", "bird", "fish", "elephant", "bee"])
        grouping = words.grouping_by(lambda w: len(w))

        # Sum of character counts per length group
        char_counts = grouping.fold(
            lambda k, e: 0,
            lambda k, acc, e: acc + len(e)
        )

        self.assertEqual(char_counts.get(3), 9)  # cat(3) + dog(3) + bee(3) = 9
        self.assertEqual(char_counts.get(4), 8)  # bird(4) + fish(4) = 8
        self.assertEqual(char_counts.get(8), 8)  # elephant(8) = 8
