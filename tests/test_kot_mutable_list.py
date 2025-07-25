import random
import unittest

from kotcollections import KotMutableList, KotMap


class TestKotMutableListBasics(unittest.TestCase):
    def test_init_empty(self):
        lst = KotMutableList()
        self.assertEqual(lst.size, 0)
        self.assertTrue(lst.is_empty())

    def test_init_with_elements(self):
        lst = KotMutableList([1, 2, 3])
        self.assertEqual(lst.size, 3)
        self.assertEqual(lst.to_list(), [1, 2, 3])

    def test_setitem(self):
        lst = KotMutableList([1, 2, 3])
        lst[1] = 10
        self.assertEqual(lst[1], 10)
        self.assertEqual(lst.to_list(), [1, 10, 3])

    def test_delitem(self):
        lst = KotMutableList([1, 2, 3, 4])
        del lst[1]
        self.assertEqual(lst.to_list(), [1, 3, 4])
        self.assertEqual(lst.size, 3)


class TestKotMutableListAdd(unittest.TestCase):
    def test_add(self):
        lst = KotMutableList()
        self.assertTrue(lst.add(1))
        self.assertTrue(lst.add(2))
        self.assertEqual(lst.to_list(), [1, 2])

    def test_add_at(self):
        lst = KotMutableList([1, 3])
        lst.add_at(1, 2)
        self.assertEqual(lst.to_list(), [1, 2, 3])

        # Add at beginning
        lst.add_at(0, 0)
        self.assertEqual(lst.to_list(), [0, 1, 2, 3])

        # Add at end
        lst.add_at(4, 4)
        self.assertEqual(lst.to_list(), [0, 1, 2, 3, 4])

        # Test index bounds
        with self.assertRaises(IndexError):
            lst.add_at(-1, 5)
        with self.assertRaises(IndexError):
            lst.add_at(6, 5)

    def test_add_all(self):
        lst = KotMutableList([1, 2])
        self.assertTrue(lst.add_all([3, 4, 5]))
        self.assertEqual(lst.to_list(), [1, 2, 3, 4, 5])

        # Add empty collection
        self.assertFalse(lst.add_all([]))
        self.assertEqual(lst.to_list(), [1, 2, 3, 4, 5])

    def test_add_all_at(self):
        lst = KotMutableList([1, 4])
        self.assertTrue(lst.add_all_at(1, [2, 3]))
        self.assertEqual(lst.to_list(), [1, 2, 3, 4])

        # Add at beginning
        self.assertTrue(lst.add_all_at(0, [-1, 0]))
        self.assertEqual(lst.to_list(), [-1, 0, 1, 2, 3, 4])

        # Add empty collection
        self.assertFalse(lst.add_all_at(2, []))
        self.assertEqual(lst.to_list(), [-1, 0, 1, 2, 3, 4])

        # Test index bounds
        with self.assertRaises(IndexError):
            lst.add_all_at(-1, [5])
        with self.assertRaises(IndexError):
            lst.add_all_at(7, [5])


class TestKotMutableListModify(unittest.TestCase):
    def test_set(self):
        lst = KotMutableList([1, 2, 3])
        old = lst.set(1, 10)
        self.assertEqual(old, 2)
        self.assertEqual(lst.to_list(), [1, 10, 3])

        # Test index bounds
        with self.assertRaises(IndexError):
            lst.set(-1, 5)
        with self.assertRaises(IndexError):
            lst.set(3, 5)

    def test_remove_at(self):
        lst = KotMutableList([1, 2, 3, 4])
        removed = lst.remove_at(1)
        self.assertEqual(removed, 2)
        self.assertEqual(lst.to_list(), [1, 3, 4])

        # Remove first
        removed = lst.remove_at(0)
        self.assertEqual(removed, 1)
        self.assertEqual(lst.to_list(), [3, 4])

        # Remove last
        removed = lst.remove_at(1)
        self.assertEqual(removed, 4)
        self.assertEqual(lst.to_list(), [3])

        # Test index bounds
        with self.assertRaises(IndexError):
            lst.remove_at(-1)
        with self.assertRaises(IndexError):
            lst.remove_at(1)

    def test_remove(self):
        lst = KotMutableList([1, 2, 3, 2, 4])
        self.assertTrue(lst.remove(2))
        self.assertEqual(lst.to_list(), [1, 3, 2, 4])  # Removes first occurrence

        self.assertTrue(lst.remove(2))
        self.assertEqual(lst.to_list(), [1, 3, 4])

        self.assertFalse(lst.remove(5))  # Element not in list
        self.assertEqual(lst.to_list(), [1, 3, 4])

    def test_remove_all(self):
        lst = KotMutableList([1, 2, 3, 2, 4, 2])
        self.assertTrue(lst.remove_all([2, 4]))
        self.assertEqual(lst.to_list(), [1, 3])

        # Remove non-existent elements
        self.assertFalse(lst.remove_all([5, 6]))
        self.assertEqual(lst.to_list(), [1, 3])

        # Remove some existing, some non-existing
        lst = KotMutableList([1, 2, 3, 4])
        self.assertTrue(lst.remove_all([2, 5]))
        self.assertEqual(lst.to_list(), [1, 3, 4])

    def test_retain_all(self):
        lst = KotMutableList([1, 2, 3, 4, 5])
        self.assertTrue(lst.retain_all([2, 4, 6]))
        self.assertEqual(lst.to_list(), [2, 4])

        # Retain all (no change)
        self.assertFalse(lst.retain_all([2, 4]))
        self.assertEqual(lst.to_list(), [2, 4])

        # Retain none
        self.assertTrue(lst.retain_all([6, 7]))
        self.assertEqual(lst.to_list(), [])

    def test_clear(self):
        lst = KotMutableList([1, 2, 3])
        lst.clear()
        self.assertEqual(lst.size, 0)
        self.assertTrue(lst.is_empty())
        self.assertEqual(lst.to_list(), [])

    def test_remove_first(self):
        lst = KotMutableList([1, 2, 3, 4, 5])
        removed = lst.remove_first()
        self.assertEqual(removed, 1)
        self.assertEqual(lst.to_list(), [2, 3, 4, 5])

        # Remove from single element list
        single = KotMutableList([42])
        self.assertEqual(single.remove_first(), 42)
        self.assertTrue(single.is_empty())

        # Remove from empty list should raise error
        empty = KotMutableList()
        with self.assertRaises(IndexError):
            empty.remove_first()

    def test_remove_last(self):
        lst = KotMutableList([1, 2, 3, 4, 5])
        removed = lst.remove_last()
        self.assertEqual(removed, 5)
        self.assertEqual(lst.to_list(), [1, 2, 3, 4])

        # Remove from single element list
        single = KotMutableList([42])
        self.assertEqual(single.remove_last(), 42)
        self.assertTrue(single.is_empty())

        # Remove from empty list should raise error
        empty = KotMutableList()
        with self.assertRaises(IndexError):
            empty.remove_last()

    def test_remove_first_or_null(self):
        lst = KotMutableList([1, 2, 3])
        self.assertEqual(lst.remove_first_or_null(), 1)
        self.assertEqual(lst.to_list(), [2, 3])

        # Remove from empty list should return None
        empty = KotMutableList()
        self.assertIsNone(empty.remove_first_or_null())

    def test_remove_first_or_none(self):
        lst = KotMutableList([1, 2, 3])
        # Verify alias returns same result as remove_first_or_null
        self.assertEqual(lst.remove_first_or_none(), 1)
        self.assertEqual(lst.to_list(), [2, 3])

        empty = KotMutableList()
        self.assertIsNone(empty.remove_first_or_none())

    def test_remove_last_or_null(self):
        lst = KotMutableList([1, 2, 3])
        self.assertEqual(lst.remove_last_or_null(), 3)
        self.assertEqual(lst.to_list(), [1, 2])

        # Remove from empty list should return None
        empty = KotMutableList()
        self.assertIsNone(empty.remove_last_or_null())

    def test_remove_last_or_none(self):
        lst = KotMutableList([1, 2, 3])
        # Verify alias returns same result as remove_last_or_null
        self.assertEqual(lst.remove_last_or_none(), 3)
        self.assertEqual(lst.to_list(), [1, 2])

        empty = KotMutableList()
        self.assertIsNone(empty.remove_last_or_none())


class TestKotMutableListSorting(unittest.TestCase):
    def test_sort(self):
        lst = KotMutableList([3, 1, 4, 1, 5])
        lst.sort()
        self.assertEqual(lst.to_list(), [1, 1, 3, 4, 5])

        # Sort with key
        lst = KotMutableList(['bb', 'aaa', 'c'])
        lst.sort(key=len)
        self.assertEqual(lst.to_list(), ['c', 'bb', 'aaa'])

        # Sort reverse
        lst = KotMutableList([3, 1, 4, 1, 5])
        lst.sort(reverse=True)
        self.assertEqual(lst.to_list(), [5, 4, 3, 1, 1])

    def test_sort_descending(self):
        lst = KotMutableList([3, 1, 4, 1, 5])
        lst.sort_descending()
        self.assertEqual(lst.to_list(), [5, 4, 3, 1, 1])

    def test_sort_by(self):
        lst = KotMutableList(['bb', 'aaa', 'c'])
        lst.sort_by(lambda x: len(x))
        self.assertEqual(lst.to_list(), ['c', 'bb', 'aaa'])

    def test_sort_by_descending(self):
        lst = KotMutableList(['bb', 'aaa', 'c'])
        lst.sort_by_descending(lambda x: len(x))
        self.assertEqual(lst.to_list(), ['aaa', 'bb', 'c'])

    def test_sort_with(self):
        # Test with custom comparator - sort by absolute value
        lst = KotMutableList([-5, -1, 3, -2, 4])
        lst.sort_with(lambda a, b: abs(a) - abs(b))
        self.assertEqual(lst.to_list(), [-1, -2, 3, 4, -5])

        # Test with string length comparison
        lst_str = KotMutableList(['aaa', 'bb', 'cccc', 'd'])
        lst_str.sort_with(lambda a, b: len(a) - len(b))
        self.assertEqual(lst_str.to_list(), ['d', 'bb', 'aaa', 'cccc'])

        # Test reverse comparison
        lst_int = KotMutableList([3, 1, 4, 1, 5])
        lst_int.sort_with(lambda a, b: b - a)
        self.assertEqual(lst_int.to_list(), [5, 4, 3, 1, 1])

    def test_reverse(self):
        lst = KotMutableList([1, 2, 3, 4, 5])
        lst.reverse()
        self.assertEqual(lst.to_list(), [5, 4, 3, 2, 1])

        # Reverse again
        lst.reverse()
        self.assertEqual(lst.to_list(), [1, 2, 3, 4, 5])

    def test_shuffle(self):
        lst = KotMutableList([1, 2, 3, 4, 5])
        original = lst.to_list()

        # Use a fixed seed for reproducible test
        rng = random.Random(42)
        lst.shuffle(rng)

        # Check that all elements are still present
        self.assertEqual(sorted(lst.to_list()), sorted(original))

        # Test without random instance
        lst2 = KotMutableList([1, 2, 3, 4, 5])
        lst2.shuffle()
        self.assertEqual(sorted(lst2.to_list()), sorted(original))


class TestKotMutableListFill(unittest.TestCase):
    def test_fill(self):
        lst = KotMutableList([1, 2, 3, 4, 5])
        lst.fill(0)
        self.assertEqual(lst.to_list(), [0, 0, 0, 0, 0])

        # Fill empty list
        empty = KotMutableList()
        empty.fill(1)
        self.assertEqual(empty.to_list(), [])


class TestKotMutableListAsReversed(unittest.TestCase):
    def test_as_reversed(self):
        lst = KotMutableList([1, 2, 3, 4, 5])
        reversed_view = lst.as_reversed()

        # Check that it's a reversed view
        self.assertEqual(reversed_view[0], 5)
        self.assertEqual(reversed_view[1], 4)
        self.assertEqual(reversed_view[4], 1)
        self.assertEqual(len(reversed_view), 5)

        # Modify through reversed view
        reversed_view[0] = 10
        self.assertEqual(lst[4], 10)  # Last element of original list
        self.assertEqual(reversed_view[0], 10)

        # Check that changes in original reflect in view
        lst[0] = 20
        self.assertEqual(reversed_view[4], 20)

        # Test accessing _elements property (for coverage)
        # This tests the internal _elements getter
        elements = reversed_view._elements
        self.assertEqual(elements, [10, 4, 3, 2, 20])


class TestKotMutableListInheritance(unittest.TestCase):
    def test_inherited_methods(self):
        # Test that KotMutableList has all KotList methods
        lst = KotMutableList([1, 2, 3, 4, 5])

        # Test some inherited methods
        self.assertEqual(lst.filter(lambda x: x % 2 == 0).to_list(), [2, 4])
        self.assertEqual(lst.map(lambda x: x * 2).to_list(), [2, 4, 6, 8, 10])
        self.assertTrue(lst.contains(3))
        self.assertEqual(lst.index_of(3), 2)

        # Test that modifications work
        lst.add(6)
        self.assertEqual(lst.size, 6)
        self.assertEqual(lst.last(), 6)


class TestKotMutableListChaining(unittest.TestCase):
    def test_method_chaining(self):
        lst = KotMutableList([5, 2, 8, 1, 9, 3])

        # Sort and then filter
        lst.sort()
        filtered = lst.filter(lambda x: x > 3)
        self.assertEqual(filtered.to_list(), [5, 8, 9])

        # Original list is sorted
        self.assertEqual(lst.to_list(), [1, 2, 3, 5, 8, 9])

    def test_complex_operations(self):
        lst = KotMutableList(['apple', 'banana', 'cherry', 'date'])

        # Add items
        lst.add('elderberry')
        lst.add_at(2, 'blueberry')

        # Sort by length
        lst.sort_by(lambda x: len(x))

        # Remove short items
        lst.retain_all([x for x in lst if len(x) > 5])

        self.assertEqual(lst.to_list(), ['banana', 'cherry', 'blueberry', 'elderberry'])


class TestKotMutableListTypeChecking(unittest.TestCase):
    def test_add_type_checking(self):
        lst = KotMutableList([1, 2, 3])

        # Add same type - should work
        lst.add(4)
        self.assertEqual(lst.to_list(), [1, 2, 3, 4])

        # Add different type - should raise TypeError
        with self.assertRaises(TypeError) as cm:
            lst.add('string')
        self.assertIn("Cannot add element of type 'str' to KotList[int]", str(cm.exception))

    def test_add_at_type_checking(self):
        lst = KotMutableList(['a', 'b', 'c'])

        # Add same type - should work
        lst.add_at(1, 'd')
        self.assertEqual(lst.to_list(), ['a', 'd', 'b', 'c'])

        # Add different type - should raise TypeError
        with self.assertRaises(TypeError) as cm:
            lst.add_at(0, 123)
        self.assertIn("Cannot add element of type 'int' to KotList[str]", str(cm.exception))

    def test_set_type_checking(self):
        lst = KotMutableList([1.0, 2.0, 3.0])

        # Set same type - should work
        lst.set(1, 5.0)
        self.assertEqual(lst.to_list(), [1.0, 5.0, 3.0])

        # Set different type - should raise TypeError
        with self.assertRaises(TypeError) as cm:
            lst.set(0, 'not a float')
        self.assertIn("Cannot add element of type 'str' to KotList[float]", str(cm.exception))

    def test_add_all_type_checking(self):
        lst = KotMutableList([1, 2])

        # Add all same type - should work
        lst.add_all([3, 4, 5])
        self.assertEqual(lst.to_list(), [1, 2, 3, 4, 5])

        # Add all with mixed types - should raise TypeError
        with self.assertRaises(TypeError) as cm:
            lst.add_all([6, 'seven', 8])
        self.assertIn("Cannot add element of type 'str' to KotList[int]", str(cm.exception))

    def test_empty_list_first_element_sets_type(self):
        lst = KotMutableList()

        # First element sets the type
        lst.add('first')
        self.assertEqual(lst._element_type, str)

        # Now only strings can be added
        lst.add('second')
        self.assertEqual(lst.to_list(), ['first', 'second'])

        # Other types should fail
        with self.assertRaises(TypeError):
            lst.add(123)


class TestKotMutableListInheritedTransformations(unittest.TestCase):
    """Test that inherited transformation methods from KotList work correctly with KotMutableList."""

    def test_associate_with_returns_kot_map(self):
        lst = KotMutableList(['a', 'bb', 'ccc'])
        assoc = lst.associate_with(lambda x: len(x))
        self.assertIsInstance(assoc, KotMap)
        self.assertEqual(assoc.to_dict(), {'a': 1, 'bb': 2, 'ccc': 3})
        # Verify KotMap methods work
        self.assertEqual(assoc.get('a'), 1)
        self.assertTrue(assoc.contains_key('bb'))

    def test_associate_by_returns_kot_map(self):
        lst = KotMutableList(['a', 'bb', 'ccc'])
        assoc = lst.associate_by(lambda x: len(x))
        self.assertIsInstance(assoc, KotMap)
        self.assertEqual(assoc.to_dict(), {1: 'a', 2: 'bb', 3: 'ccc'})
        # Verify KotMap methods work
        self.assertEqual(assoc.get(2), 'bb')
        self.assertTrue(assoc.contains_key(3))

    def test_associate_by_with_value_returns_kot_map(self):
        lst = KotMutableList(['a', 'bb', 'ccc'])
        assoc = lst.associate_by_with_value(lambda x: len(x), lambda x: x.upper())
        self.assertIsInstance(assoc, KotMap)
        self.assertEqual(assoc.to_dict(), {1: 'A', 2: 'BB', 3: 'CCC'})
        # Verify KotMap methods work
        self.assertEqual(assoc.get(1), 'A')
        self.assertTrue(assoc.contains_key(2))

    def test_group_by_returns_kot_map(self):
        lst = KotMutableList([1, 2, 3, 4, 5, 6])
        grouped = lst.group_by(lambda x: x % 2)
        self.assertIsInstance(grouped, KotMap)
        self.assertEqual(grouped.get(0).to_list(), [2, 4, 6])
        self.assertEqual(grouped.get(1).to_list(), [1, 3, 5])
        # Verify KotMap methods work
        self.assertTrue(grouped.contains_key(0))
        self.assertTrue(grouped.contains_key(1))
        # Verify values are KotList instances
        from kotcollections import KotList
        self.assertIsInstance(grouped.get(0), KotList)  # Should be KotList

    def test_group_by_with_value_returns_kot_map(self):
        from kotcollections import KotList
        lst = KotMutableList(['a', 'bb', 'ccc', 'dd', 'e'])
        grouped = lst.group_by_with_value(lambda x: len(x), lambda x: x.upper())
        self.assertIsInstance(grouped, KotMap)
        self.assertEqual(grouped.get(1).to_list(), ['A', 'E'])
        self.assertEqual(grouped.get(2).to_list(), ['BB', 'DD'])
        self.assertEqual(grouped.get(3).to_list(), ['CCC'])
        # Verify KotMap methods work
        self.assertTrue(grouped.contains_key(1))
        self.assertEqual(set(grouped.keys), {1, 2, 3})
        # Verify values are KotList instances
        self.assertIsInstance(grouped.get(1), KotList)  # Should be KotList


class TestKotMutableListTypeSpecification(unittest.TestCase):
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

        # Test creating typed KotMutableList with parent type
        animals = KotMutableList[Animal]()
        self.assertEqual(len(animals), 0)

        # Add different subclass instances
        animals.add(Dog("Buddy"))
        animals.add(Cat("Whiskers"))
        self.assertEqual(len(animals), 2)

        # Test with initial elements
        animals2 = KotMutableList[Animal]([Dog("Max"), Cat("Luna")])
        self.assertEqual(len(animals2), 2)
        self.assertIsInstance(animals2[0], Dog)
        self.assertIsInstance(animals2[1], Cat)

        # Add more animals
        animals2.add(Dog("Rex"))
        self.assertEqual(len(animals2), 3)

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

        # Test creating empty typed KotMutableList
        animals = KotMutableList.of_type(Animal)
        self.assertEqual(len(animals), 0)

        # Add different subclass instances
        animals.add(Dog("Buddy"))
        animals.add(Cat("Whiskers"))
        self.assertEqual(len(animals), 2)

        # Test with initial elements
        animals2 = KotMutableList.of_type(Animal, [Dog("Max"), Cat("Luna")])
        self.assertEqual(len(animals2), 2)
        self.assertIsInstance(animals2[0], Dog)
        self.assertIsInstance(animals2[1], Cat)

        # Test type checking is enforced
        class NotAnimal:
            pass

        with self.assertRaises(TypeError):
            animals2.add(NotAnimal())

    def test_type_preservation_in_conversions(self):
        """Test that type information is preserved during conversions"""

        # Define test classes with inheritance
        class Animal:
            def __init__(self, name):
                self.name = name

        class Dog(Animal):
            pass

        # Test KotMutableList type preservation
        animals = KotMutableList.of_type(Animal, [Dog("Buddy")])
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
