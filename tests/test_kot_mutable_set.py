"""
Unit tests for KotMutableSet class.
"""

import unittest

from kotcollections.kot_list import KotList
from kotcollections.kot_map import KotMap
from kotcollections.kot_mutable_set import KotMutableSet
from kotcollections.kot_set import KotSet


class TestKotMutableSetBasics(unittest.TestCase):
    """Test basic KotMutableSet functionality."""

    def test_init_empty(self):
        """Test creating an empty KotMutableSet."""
        s = KotMutableSet()
        self.assertTrue(s.is_empty())
        self.assertEqual(s.size, 0)
        self.assertEqual(list(s), [])

    def test_init_from_set(self):
        """Test creating KotMutableSet from a Python set."""
        s = KotMutableSet({1, 2, 3})
        self.assertFalse(s.is_empty())
        self.assertEqual(s.size, 3)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)

    def test_init_from_list(self):
        """Test creating KotMutableSet from a list."""
        s = KotMutableSet([1, 2, 2, 3, 3, 3])
        self.assertEqual(s.size, 3)  # Duplicates removed
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)

    def test_repr(self):
        """Test string representation."""
        s = KotMutableSet([1, 2, 3])
        repr_str = repr(s)
        self.assertTrue(repr_str.startswith("KotMutableSet("))
        self.assertTrue("1" in repr_str)
        self.assertTrue("2" in repr_str)
        self.assertTrue("3" in repr_str)

    def test_inherits_from_kot_set(self):
        """Test that KotMutableSet inherits from KotSet."""
        s = KotMutableSet([1, 2, 3])
        self.assertIsInstance(s, KotSet)


class TestKotMutableSetMutations(unittest.TestCase):
    """Test KotMutableSet mutation operations."""

    def test_add(self):
        """Test add operation."""
        s = KotMutableSet()

        # Add to empty set
        self.assertTrue(s.add(1))
        self.assertEqual(s.size, 1)
        self.assertTrue(1 in s)

        # Add more elements
        self.assertTrue(s.add(2))
        self.assertTrue(s.add(3))
        self.assertEqual(s.size, 3)

        # Try to add duplicate
        self.assertFalse(s.add(1))
        self.assertEqual(s.size, 3)

    def test_add_type_safety(self):
        """Test add maintains type safety."""
        s = KotMutableSet([1, 2, 3])

        with self.assertRaises(TypeError):
            s.add("4")

    def test_add_all(self):
        """Test add_all operation."""
        s = KotMutableSet([1, 2, 3])

        # Add from set
        self.assertTrue(s.add_all({3, 4, 5}))
        self.assertEqual(s.size, 5)

        # Add from list with no new elements
        self.assertFalse(s.add_all([1, 2, 3]))
        self.assertEqual(s.size, 5)

        # Add from KotSet
        other = KotSet([5, 6, 7])
        self.assertTrue(s.add_all(other))
        self.assertEqual(s.size, 7)

    def test_remove(self):
        """Test remove operation."""
        s = KotMutableSet([1, 2, 3, 4, 5])

        # Remove existing element
        self.assertTrue(s.remove(3))
        self.assertEqual(s.size, 4)
        self.assertFalse(3 in s)

        # Try to remove non-existing element
        self.assertFalse(s.remove(10))
        self.assertEqual(s.size, 4)

        # Remove all elements
        for i in [1, 2, 4, 5]:
            self.assertTrue(s.remove(i))
        self.assertTrue(s.is_empty())

    def test_remove_all(self):
        """Test remove_all operation."""
        s = KotMutableSet([1, 2, 3, 4, 5])

        # Remove multiple elements
        self.assertTrue(s.remove_all({2, 3, 4}))
        self.assertEqual(s.size, 2)
        self.assertTrue(1 in s)
        self.assertTrue(5 in s)

        # Try to remove non-existing elements
        self.assertFalse(s.remove_all({10, 11, 12}))
        self.assertEqual(s.size, 2)

        # Remove from list
        self.assertTrue(s.remove_all([1, 5]))
        self.assertTrue(s.is_empty())

        # Test with KotSet
        s2 = KotMutableSet([1, 2, 3, 4, 5])
        kot_set_to_remove = KotSet([2, 3, 4])
        self.assertTrue(s2.remove_all(kot_set_to_remove))
        self.assertEqual(s2.size, 2)

    def test_retain_all(self):
        """Test retain_all operation."""
        s = KotMutableSet([1, 2, 3, 4, 5])

        # Retain subset
        self.assertTrue(s.retain_all({2, 3, 4}))
        self.assertEqual(s.size, 3)
        self.assertFalse(1 in s)
        self.assertFalse(5 in s)

        # Retain with no changes
        self.assertFalse(s.retain_all({2, 3, 4, 6, 7}))
        self.assertEqual(s.size, 3)

        # Retain empty set
        self.assertTrue(s.retain_all(set()))
        self.assertTrue(s.is_empty())

        # Test with KotSet
        s2 = KotMutableSet([1, 2, 3, 4, 5])
        kot_set_to_retain = KotSet([2, 3, 4])
        self.assertTrue(s2.retain_all(kot_set_to_retain))
        self.assertEqual(s2.size, 3)

        # Test with list
        s3 = KotMutableSet([1, 2, 3, 4, 5])
        self.assertTrue(s3.retain_all([1, 2, 3]))
        self.assertEqual(s3.size, 3)
        self.assertTrue(all(x in [1, 2, 3] for x in s3))

    def test_clear(self):
        """Test clear operation."""
        s = KotMutableSet([1, 2, 3, 4, 5])
        self.assertEqual(s.size, 5)

        s.clear()
        self.assertTrue(s.is_empty())
        self.assertEqual(s.size, 0)

        # Can add after clear
        self.assertTrue(s.add(10))
        self.assertEqual(s.size, 1)

    def test_remove_if(self):
        """Test remove_if operation."""
        s = KotMutableSet([1, 2, 3, 4, 5, 6])

        # Remove even numbers
        self.assertTrue(s.remove_if(lambda x: x % 2 == 0))
        self.assertEqual(s.size, 3)
        self.assertTrue(all(x % 2 == 1 for x in s))

        # Try to remove with no matches
        self.assertFalse(s.remove_if(lambda x: x > 10))
        self.assertEqual(s.size, 3)

        # Remove all
        self.assertTrue(s.remove_if(lambda x: True))
        self.assertTrue(s.is_empty())

    def test_retain_if(self):
        """Test retain_if operation."""
        s = KotMutableSet([1, 2, 3, 4, 5, 6])

        # Retain even numbers
        self.assertTrue(s.retain_if(lambda x: x % 2 == 0))
        self.assertEqual(s.size, 3)
        self.assertTrue(all(x % 2 == 0 for x in s))

        # Retain all (no change)
        self.assertFalse(s.retain_if(lambda x: x > 0))
        self.assertEqual(s.size, 3)

        # Retain none
        self.assertTrue(s.retain_if(lambda x: False))
        self.assertTrue(s.is_empty())


class TestKotMutableSetSetOperations(unittest.TestCase):
    """Test KotMutableSet set operations with mutation."""

    def test_union_update(self):
        """Test union_update operation."""
        s = KotMutableSet([1, 2, 3])
        s.union_update({3, 4, 5})

        self.assertEqual(s.size, 5)
        for i in range(1, 6):
            self.assertTrue(i in s)

        # Union with KotSet
        other = KotSet([5, 6, 7])
        s.union_update(other)
        self.assertEqual(s.size, 7)

    def test_intersect_update(self):
        """Test intersect_update operation."""
        s = KotMutableSet([1, 2, 3, 4, 5])
        s.intersect_update({3, 4, 5, 6, 7})

        self.assertEqual(s.size, 3)
        self.assertTrue(3 in s)
        self.assertTrue(4 in s)
        self.assertTrue(5 in s)

        # Intersect with empty
        s.intersect_update(set())
        self.assertTrue(s.is_empty())

    def test_subtract_update(self):
        """Test subtract_update operation."""
        s = KotMutableSet([1, 2, 3, 4, 5])
        s.subtract_update({3, 4, 5, 6, 7})

        self.assertEqual(s.size, 2)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)

        # Subtract all
        s.subtract_update({1, 2})
        self.assertTrue(s.is_empty())


class TestKotMutableSetOperators(unittest.TestCase):
    """Test KotMutableSet operator overloads."""

    def test_iadd_operator(self):
        """Test += operator (union update)."""
        s = KotMutableSet([1, 2, 3])
        s += {3, 4, 5}

        self.assertEqual(s.size, 5)
        for i in range(1, 6):
            self.assertTrue(i in s)

        # Chain operations
        s += KotSet([6, 7])
        self.assertEqual(s.size, 7)

    def test_isub_operator(self):
        """Test -= operator (subtract update)."""
        s = KotMutableSet([1, 2, 3, 4, 5])
        s -= {3, 4}

        self.assertEqual(s.size, 3)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(5 in s)

        # Chain operations
        s -= KotSet([1, 5])
        self.assertEqual(s.size, 1)
        self.assertTrue(2 in s)

    def test_iand_operator(self):
        """Test &= operator (intersect update)."""
        s = KotMutableSet([1, 2, 3, 4, 5])
        s &= {3, 4, 5, 6, 7}

        self.assertEqual(s.size, 3)
        self.assertTrue(3 in s)
        self.assertTrue(4 in s)
        self.assertTrue(5 in s)

        # Chain operations
        s &= KotSet([4, 5])
        self.assertEqual(s.size, 2)


class TestKotMutableSetConversion(unittest.TestCase):
    """Test KotMutableSet conversion operations."""

    def test_to_kot_set(self):
        """Test conversion to immutable KotSet."""
        ms = KotMutableSet([1, 2, 3])
        s = ms.to_kot_set()

        # Check it's a KotSet
        self.assertIsInstance(s, KotSet)
        self.assertNotIsInstance(s, KotMutableSet)

        # Check contents are copied
        self.assertEqual(s.size, 3)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)

        # Ensure it's a copy
        ms.add(4)
        self.assertEqual(ms.size, 4)
        self.assertEqual(s.size, 3)


class TestKotMutableSetTypeManagement(unittest.TestCase):
    """Test type management during mutations."""

    def test_type_reset_on_clear(self):
        """Test that type is reset when set is cleared."""
        s = KotMutableSet([1, 2, 3])
        s.clear()

        # Should be able to add strings now
        self.assertTrue(s.add("hello"))
        self.assertTrue(s.add("world"))
        self.assertEqual(s.size, 2)

    def test_type_reset_on_remove_all(self):
        """Test that type is reset when all elements are removed."""
        s = KotMutableSet([1, 2, 3])
        s.remove_all([1, 2, 3])

        # Should be able to add strings now
        self.assertTrue(s.add("hello"))
        self.assertEqual(s.size, 1)

    def test_type_preserved_partial_remove(self):
        """Test that type is preserved when some elements remain."""
        s = KotMutableSet([1, 2, 3])
        s.remove(1)

        # Should still enforce integer type
        with self.assertRaises(TypeError):
            s.add("4")

        # Can add more integers
        self.assertTrue(s.add(4))
        self.assertEqual(s.size, 3)


class TestKotMutableSetWithKotList(unittest.TestCase):
    """Test KotMutableSet accepting KotList and KotMutableList."""

    def test_init_from_kot_list(self):
        """Test creating KotMutableSet from KotList."""
        from kotcollections.kot_list import KotList

        kot_list = KotList([1, 2, 2, 3, 3, 3])
        s = KotMutableSet(kot_list)
        self.assertEqual(s.size, 3)  # Duplicates removed
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)

        # Test mutation after creation
        self.assertTrue(s.add(4))
        self.assertEqual(s.size, 4)

    def test_add_all_with_kot_list(self):
        """Test add_all with KotList."""
        from kotcollections.kot_list import KotList

        s = KotMutableSet([1, 2])
        kot_list = KotList([2, 3, 4])
        self.assertTrue(s.add_all(kot_list))
        self.assertEqual(s.size, 4)
        self.assertTrue(3 in s)
        self.assertTrue(4 in s)

        # Test with KotMutableList
        from kotcollections.kot_mutable_list import KotMutableList
        kot_mutable_list = KotMutableList([4, 5, 6])
        self.assertTrue(s.add_all(kot_mutable_list))
        self.assertEqual(s.size, 6)

    def test_remove_all_with_kot_list(self):
        """Test remove_all with KotList."""
        from kotcollections.kot_list import KotList

        s = KotMutableSet([1, 2, 3, 4, 5])
        kot_list = KotList([2, 3, 4])
        self.assertTrue(s.remove_all(kot_list))
        self.assertEqual(s.size, 2)
        self.assertTrue(1 in s)
        self.assertTrue(5 in s)

    def test_retain_all_with_kot_list(self):
        """Test retain_all with KotList."""
        from kotcollections.kot_list import KotList

        s = KotMutableSet([1, 2, 3, 4, 5])
        kot_list = KotList([2, 3, 4, 6])
        self.assertTrue(s.retain_all(kot_list))
        self.assertEqual(s.size, 3)
        self.assertTrue(2 in s)
        self.assertTrue(3 in s)
        self.assertTrue(4 in s)

    def test_union_update_with_kot_list(self):
        """Test union_update with KotList."""
        from kotcollections.kot_list import KotList

        s = KotMutableSet([1, 2, 3])
        kot_list = KotList([3, 4, 5, 5])
        s.union_update(kot_list)

        self.assertEqual(s.size, 5)
        for i in range(1, 6):
            self.assertTrue(i in s)

    def test_intersect_update_with_kot_list(self):
        """Test intersect_update with KotList."""
        from kotcollections.kot_list import KotList

        s = KotMutableSet([1, 2, 3, 4, 5])
        kot_list = KotList([3, 4, 5, 6, 7])
        s.intersect_update(kot_list)

        self.assertEqual(s.size, 3)
        self.assertTrue(3 in s)
        self.assertTrue(4 in s)
        self.assertTrue(5 in s)

    def test_subtract_update_with_kot_list(self):
        """Test subtract_update with KotList."""
        from kotcollections.kot_list import KotList

        s = KotMutableSet([1, 2, 3, 4, 5])
        kot_list = KotList([3, 4, 5])
        s.subtract_update(kot_list)

        self.assertEqual(s.size, 2)
        self.assertTrue(1 in s)
        self.assertTrue(2 in s)

    def test_operators_with_kot_list(self):
        """Test operators +=, -=, &= with KotList."""
        from kotcollections.kot_list import KotList
        from kotcollections.kot_mutable_list import KotMutableList

        # Test += operator
        s1 = KotMutableSet([1, 2, 3])
        kot_list1 = KotList([3, 4, 5])
        s1 += kot_list1
        self.assertEqual(s1.size, 5)

        # Test -= operator
        s2 = KotMutableSet([1, 2, 3, 4, 5])
        kot_list2 = KotMutableList([3, 4])
        s2 -= kot_list2
        self.assertEqual(s2.size, 3)
        self.assertTrue(1 in s2)
        self.assertTrue(2 in s2)
        self.assertTrue(5 in s2)

        # Test &= operator
        s3 = KotMutableSet([1, 2, 3, 4, 5])
        kot_list3 = KotList([3, 4, 5, 6])
        s3 &= kot_list3
        self.assertEqual(s3.size, 3)
        for i in [3, 4, 5]:
            self.assertTrue(i in s3)


class TestKotMutableSetInheritedTransformations(unittest.TestCase):
    """Test that inherited transformation methods from KotSet work correctly with KotMutableSet."""

    def test_group_by_returns_kot_map(self):
        """Test group_by returns KotMap."""
        s = KotMutableSet([1, 2, 3, 4, 5, 6])
        groups = s.group_by(lambda x: x % 2)

        self.assertIsInstance(groups, KotMap)
        self.assertEqual(groups.size, 2)

        evens = groups.get(0)
        odds = groups.get(1)
        self.assertIsInstance(evens, KotSet)
        self.assertIsInstance(odds, KotSet)

        self.assertEqual(evens.size, 3)
        self.assertEqual(odds.size, 3)

        # Verify KotMap methods work
        self.assertTrue(groups.contains_key(0))
        self.assertTrue(groups.contains_key(1))
        self.assertEqual(set(groups.keys), {0, 1})

    def test_group_by_to_returns_kot_map(self):
        """Test group_by_to returns KotMap with KotList values."""
        s = KotMutableSet(['apple', 'apricot', 'banana', 'blueberry'])
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

        # Verify KotMap methods work
        self.assertEqual(set(result.keys), {'a', 'b'})

    def test_associate_returns_kot_map(self):
        """Test associate returns KotMap."""
        s = KotMutableSet([1, 2, 3])
        result = s.associate(lambda x: (x, x * x))

        self.assertIsInstance(result, KotMap)
        self.assertEqual(result.to_dict(), {1: 1, 2: 4, 3: 9})

        # Verify KotMap methods work
        self.assertEqual(result.get(2), 4)
        self.assertTrue(result.contains_key(3))
        self.assertEqual(set(result.keys), {1, 2, 3})

    def test_associate_by_returns_kot_map(self):
        """Test associate_by returns KotMap."""
        s = KotMutableSet(["hello", "world", "test"])
        result = s.associate_by(len)

        self.assertIsInstance(result, KotMap)
        self.assertEqual(result.get(4), "test")
        self.assertIn(result.get(5), ["hello", "world"])

        # Verify KotMap methods work
        self.assertTrue(result.contains_key(4))
        self.assertTrue(result.contains_key(5))
        self.assertEqual(set(result.keys), {4, 5})

    def test_associate_with_returns_kot_map(self):
        """Test associate_with returns KotMap."""
        s = KotMutableSet([1, 2, 3])
        result = s.associate_with(lambda x: x * x)

        self.assertIsInstance(result, KotMap)
        self.assertEqual(result.to_dict(), {1: 1, 2: 4, 3: 9})

        # Verify KotMap methods work
        self.assertEqual(result.get(2), 4)
        self.assertTrue(result.contains_key(1))
        self.assertEqual(set(result.values), {1, 4, 9})


class TestKotMutableSetTypeSpecification(unittest.TestCase):
    def test_class_getitem_syntax(self):
        """Test __class_getitem__ for type specification"""
        # Define test classes with inheritance
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
        
        # Test creating typed KotMutableSet with parent type
        animals = KotMutableSet[Animal]()
        self.assertEqual(len(animals), 0)
        
        # Add different subclass instances
        animals.add(Dog("Buddy"))
        animals.add(Cat("Whiskers"))
        self.assertEqual(len(animals), 2)
        
        # Test with initial elements
        animals2 = KotMutableSet[Animal]([Dog("Max"), Cat("Luna")])
        self.assertEqual(len(animals2), 2)
        self.assertTrue(any(isinstance(elem, Dog) and elem.name == "Max" for elem in animals2))
        self.assertTrue(any(isinstance(elem, Cat) and elem.name == "Luna" for elem in animals2))
        
        # Add more animals
        animals2.add(Dog("Rex"))
        self.assertEqual(len(animals2), 3)
    
    def test_of_type_method(self):
        """Test of_type class method for type specification"""
        # Define test classes with inheritance
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
        
        # Test creating empty typed KotMutableSet
        animals = KotMutableSet.of_type(Animal)
        self.assertEqual(len(animals), 0)
        
        # Add different subclass instances
        animals.add(Dog("Buddy"))
        animals.add(Cat("Whiskers"))
        self.assertEqual(len(animals), 2)
        
        # Test with initial elements (list)
        animals2 = KotMutableSet.of_type(Animal, [Dog("Max"), Cat("Luna")])
        self.assertEqual(len(animals2), 2)
        self.assertTrue(any(isinstance(elem, Dog) and elem.name == "Max" for elem in animals2))
        self.assertTrue(any(isinstance(elem, Cat) and elem.name == "Luna" for elem in animals2))
        
        # Test with initial elements (set)
        animals3 = KotMutableSet.of_type(Animal, {Dog("Rex"), Cat("Mittens")})
        self.assertEqual(len(animals3), 2)
        self.assertTrue(any(isinstance(elem, Dog) and elem.name == "Rex" for elem in animals3))
        self.assertTrue(any(isinstance(elem, Cat) and elem.name == "Mittens" for elem in animals3))
        
        # Test type checking is enforced
        class NotAnimal:
            pass
        
        with self.assertRaises(TypeError):
            animals3.add(NotAnimal())
