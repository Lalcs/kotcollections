"""
Unit tests for KotMutableMap class.
"""

import unittest

from kotcollections.kot_map import KotMap
from kotcollections.kot_mutable_map import KotMutableMap


class TestKotMutableMapBasics(unittest.TestCase):
    """Test basic KotMutableMap functionality."""

    def test_inherits_from_kot_map(self):
        """Test that KotMutableMap inherits from KotMap."""
        m = KotMutableMap()
        self.assertIsInstance(m, KotMap)

    def test_init_empty(self):
        """Test creating an empty KotMutableMap."""
        m = KotMutableMap()
        self.assertTrue(m.is_empty())
        self.assertEqual(m.size, 0)

    def test_init_from_dict(self):
        """Test creating KotMutableMap from a dict."""
        m = KotMutableMap({"a": 1, "b": 2, "c": 3})
        self.assertEqual(m.size, 3)
        self.assertEqual(m.get("a"), 1)
        self.assertEqual(m.get("b"), 2)
        self.assertEqual(m.get("c"), 3)

    def test_type_safety_maintained(self):
        """Test that type safety is maintained in mutable operations."""
        m = KotMutableMap({"a": 1, "b": 2})
        
        # Adding same types should work
        m.put("c", 3)
        self.assertEqual(m.get("c"), 3)
        
        # Adding different value type should fail
        with self.assertRaises(TypeError):
            m.put("d", "not an int")
        
        # Adding different key type should fail
        with self.assertRaises(TypeError):
            m.put(4, 4)


class TestKotMutableMapPutOperations(unittest.TestCase):
    """Test KotMutableMap put operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMutableMap({"a": 1, "b": 2})

    def test_put(self):
        """Test put method."""
        # Add new entry
        old = self.map.put("c", 3)
        self.assertIsNone(old)
        self.assertEqual(self.map.get("c"), 3)
        self.assertEqual(self.map.size, 3)
        
        # Replace existing entry
        old = self.map.put("a", 10)
        self.assertEqual(old, 1)
        self.assertEqual(self.map.get("a"), 10)
        self.assertEqual(self.map.size, 3)

    def test_put_all(self):
        """Test put_all method."""
        # From dict
        self.map.put_all({"c": 3, "d": 4})
        self.assertEqual(self.map.size, 4)
        self.assertEqual(self.map.get("c"), 3)
        self.assertEqual(self.map.get("d"), 4)
        
        # From KotMap
        other = KotMap({"e": 5, "f": 6})
        self.map.put_all(other)
        self.assertEqual(self.map.size, 6)
        self.assertEqual(self.map.get("e"), 5)
        self.assertEqual(self.map.get("f"), 6)
        
        # From list of tuples
        self.map.put_all([("g", 7), ("h", 8)])
        self.assertEqual(self.map.size, 8)
        self.assertEqual(self.map.get("g"), 7)
        self.assertEqual(self.map.get("h"), 8)

    def test_put_if_absent(self):
        """Test put_if_absent method."""
        # Add new entry
        result = self.map.put_if_absent("c", 3)
        self.assertIsNone(result)
        self.assertEqual(self.map.get("c"), 3)
        
        # Try to add existing entry
        result = self.map.put_if_absent("a", 10)
        self.assertEqual(result, 1)  # Returns existing value
        self.assertEqual(self.map.get("a"), 1)  # Value not changed

    def test_setitem(self):
        """Test __setitem__ ([] operator)."""
        self.map["c"] = 3
        self.assertEqual(self.map.get("c"), 3)
        
        self.map["a"] = 10
        self.assertEqual(self.map.get("a"), 10)


class TestKotMutableMapRemoveOperations(unittest.TestCase):
    """Test KotMutableMap remove operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMutableMap({"a": 1, "b": 2, "c": 3, "d": 4})

    def test_remove(self):
        """Test remove method."""
        # Remove existing key
        value = self.map.remove("b")
        self.assertEqual(value, 2)
        self.assertEqual(self.map.size, 3)
        self.assertFalse(self.map.contains_key("b"))
        
        # Remove non-existing key
        value = self.map.remove("z")
        self.assertIsNone(value)
        self.assertEqual(self.map.size, 3)

    def test_remove_value(self):
        """Test remove_value method."""
        # Remove with matching value
        result = self.map.remove_value("b", 2)
        self.assertTrue(result)
        self.assertFalse(self.map.contains_key("b"))
        
        # Try to remove with non-matching value
        result = self.map.remove_value("c", 99)
        self.assertFalse(result)
        self.assertTrue(self.map.contains_key("c"))
        
        # Try to remove non-existing key
        result = self.map.remove_value("z", 99)
        self.assertFalse(result)

    def test_clear(self):
        """Test clear method."""
        self.map.clear()
        self.assertTrue(self.map.is_empty())
        self.assertEqual(self.map.size, 0)
        
        # Can add new elements after clear
        self.map.put("x", 10)
        self.assertEqual(self.map.get("x"), 10)

    def test_delitem(self):
        """Test __delitem__ (del operator)."""
        del self.map["b"]
        self.assertFalse(self.map.contains_key("b"))
        self.assertEqual(self.map.size, 3)
        
        with self.assertRaises(KeyError):
            del self.map["z"]

    def test_pop(self):
        """Test pop method."""
        # Pop existing key
        value = self.map.pop("b")
        self.assertEqual(value, 2)
        self.assertFalse(self.map.contains_key("b"))
        
        # Pop with default
        value = self.map.pop("z", 99)
        self.assertEqual(value, 99)
        
        # Pop without default raises KeyError
        with self.assertRaises(KeyError):
            self.map.pop("z")

    def test_popitem(self):
        """Test popitem method."""
        initial_size = self.map.size
        key, value = self.map.popitem()
        
        self.assertIsNotNone(key)
        self.assertIsNotNone(value)
        self.assertEqual(self.map.size, initial_size - 1)
        self.assertFalse(self.map.contains_key(key))
        
        # Empty map
        empty = KotMutableMap()
        with self.assertRaises(KeyError):
            empty.popitem()


class TestKotMutableMapAdvancedOperations(unittest.TestCase):
    """Test KotMutableMap advanced operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMutableMap({"a": 1, "b": 2})

    def test_get_or_put(self):
        """Test get_or_put method."""
        # Get existing value
        counter = 0
        def create_value():
            nonlocal counter
            counter += 1
            return 99
        
        value = self.map.get_or_put("a", create_value)
        self.assertEqual(value, 1)
        self.assertEqual(counter, 0)  # Lambda not called
        
        # Put new value
        value = self.map.get_or_put("c", create_value)
        self.assertEqual(value, 99)
        self.assertEqual(counter, 1)  # Lambda called
        self.assertEqual(self.map.get("c"), 99)

    def test_compute(self):
        """Test compute method."""
        # Update existing value
        result = self.map.compute("a", lambda k, v: v * 10 if v else 0)
        self.assertEqual(result, 10)
        self.assertEqual(self.map.get("a"), 10)
        
        # Add new value
        result = self.map.compute("c", lambda k, v: 3 if v is None else v)
        self.assertEqual(result, 3)
        self.assertEqual(self.map.get("c"), 3)
        
        # Remove by returning None
        result = self.map.compute("b", lambda k, v: None)
        self.assertIsNone(result)
        self.assertFalse(self.map.contains_key("b"))

    def test_compute_if_absent(self):
        """Test compute_if_absent method."""
        # Existing key - function not called
        counter = 0
        def create_value(key):
            nonlocal counter
            counter += 1
            return 99
        
        result = self.map.compute_if_absent("a", create_value)
        self.assertEqual(result, 1)
        self.assertEqual(counter, 0)
        
        # New key - function called
        result = self.map.compute_if_absent("c", create_value)
        self.assertEqual(result, 99)
        self.assertEqual(counter, 1)
        self.assertEqual(self.map.get("c"), 99)

    def test_compute_if_present(self):
        """Test compute_if_present method."""
        # Existing key
        result = self.map.compute_if_present("a", lambda k, v: v * 10)
        self.assertEqual(result, 10)
        self.assertEqual(self.map.get("a"), 10)
        
        # Non-existing key - function not called
        result = self.map.compute_if_present("z", lambda k, v: 99)
        self.assertIsNone(result)
        self.assertFalse(self.map.contains_key("z"))
        
        # Remove by returning None
        result = self.map.compute_if_present("b", lambda k, v: None)
        self.assertIsNone(result)
        self.assertFalse(self.map.contains_key("b"))

    def test_replace(self):
        """Test replace method."""
        # Replace existing key
        old = self.map.replace("a", 10)
        self.assertEqual(old, 1)
        self.assertEqual(self.map.get("a"), 10)
        
        # Try to replace non-existing key
        old = self.map.replace("z", 99)
        self.assertIsNone(old)
        self.assertFalse(self.map.contains_key("z"))

    def test_replace_all(self):
        """Test replace_all method."""
        self.map.replace_all(lambda k, v: v * 10)
        self.assertEqual(self.map.get("a"), 10)
        self.assertEqual(self.map.get("b"), 20)

    def test_merge(self):
        """Test merge method."""
        # Merge with new key
        result = self.map.merge("c", 3, lambda old, new: old + new)
        self.assertEqual(result, 3)
        self.assertEqual(self.map.get("c"), 3)
        
        # Merge with existing key
        result = self.map.merge("a", 10, lambda old, new: old + new)
        self.assertEqual(result, 11)
        self.assertEqual(self.map.get("a"), 11)


class TestKotMutableMapBulkOperations(unittest.TestCase):
    """Test KotMutableMap bulk operations."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMutableMap({"a": 1, "b": 2})

    def test_plus_assign(self):
        """Test plus_assign method."""
        # With dict
        self.map.plus_assign({"c": 3, "d": 4})
        self.assertEqual(self.map.size, 4)
        
        # With KotMap
        other = KotMap({"e": 5, "f": 6})
        self.map.plus_assign(other)
        self.assertEqual(self.map.size, 6)
        
        # With single tuple
        self.map.plus_assign(("g", 7))
        self.assertEqual(self.map.size, 7)
        self.assertEqual(self.map.get("g"), 7)

    def test_minus_assign(self):
        """Test minus_assign method."""
        self.map.minus_assign("a")
        self.assertFalse(self.map.contains_key("a"))
        self.assertEqual(self.map.size, 1)

    def test_update(self):
        """Test update method."""
        # Update from dict
        self.map.update({"a": 10, "c": 3})
        self.assertEqual(self.map.get("a"), 10)  # Updated
        self.assertEqual(self.map.get("b"), 2)   # Unchanged
        self.assertEqual(self.map.get("c"), 3)   # Added
        
        # Update from KotMap
        other = KotMap({"b": 20, "d": 4})
        self.map.update(other)
        self.assertEqual(self.map.get("b"), 20)  # Updated
        self.assertEqual(self.map.get("d"), 4)   # Added
        
        # Update from list of tuples
        self.map.update([("e", 5), ("f", 6)])
        self.assertEqual(self.map.size, 6)


class TestKotMutableMapTypeResets(unittest.TestCase):
    """Test that type constraints are properly reset when map becomes empty."""

    def test_type_reset_on_clear(self):
        """Test type reset when clear is called."""
        m = KotMutableMap({"a": 1, "b": 2})
        m.clear()
        
        # Should be able to add different types now
        m.put("x", "string")
        self.assertEqual(m.get("x"), "string")

    def test_type_reset_on_remove(self):
        """Test type reset when all elements are removed."""
        m = KotMutableMap({"a": 1, "b": 2})
        m.remove("a")
        m.remove("b")
        
        # Should be able to add different types now
        m.put(1, "string")
        self.assertEqual(m.get(1), "string")

    def test_type_maintained_when_not_empty(self):
        """Test that types are maintained when map is not empty."""
        m = KotMutableMap({"a": 1, "b": 2})
        m.remove("a")
        
        # Should still enforce types
        with self.assertRaises(TypeError):
            m.put("c", "string")


class TestKotMutableMapInheritedMethods(unittest.TestCase):
    """Test that KotMutableMap properly inherits KotMap methods."""

    def setUp(self):
        """Set up test data."""
        self.map = KotMutableMap({"a": 1, "b": 2, "c": 3})

    def test_filtering_returns_kot_map(self):
        """Test that filtering methods return KotMap instances."""
        filtered = self.map.filter(lambda k, v: v > 1)
        self.assertIsInstance(filtered, KotMap)
        self.assertNotIsInstance(filtered, KotMutableMap)

    def test_transformation_returns_kot_map(self):
        """Test that transformation methods return KotMap instances."""
        mapped = self.map.map_values(lambda k, v: v * 10)
        self.assertIsInstance(mapped, KotMap)
        self.assertNotIsInstance(mapped, KotMutableMap)

    def test_immutable_operations_work(self):
        """Test that all immutable operations work correctly."""
        self.assertTrue(self.map.contains_key("a"))
        self.assertTrue(self.map.contains_value(2))
        self.assertEqual(self.map.get_or_default("z", 99), 99)
        self.assertTrue(self.map.all(lambda k, v: v > 0))
        self.assertTrue(self.map.any(lambda k, v: v == 2))
        self.assertEqual(self.map.count(lambda k, v: v > 1), 2)

    def test_mutable_map_is_not_hashable(self):
        """Test that KotMutableMap cannot be hashed."""
        with self.assertRaises(TypeError):
            hash(self.map)
        
        # Cannot be used in sets
        with self.assertRaises(TypeError):
            s = {self.map}


class TestKotMutableMapEdgeCases(unittest.TestCase):
    """Test KotMutableMap edge cases."""

    def test_operations_on_empty_map(self):
        """Test mutation operations on empty map."""
        m = KotMutableMap()
        
        # Remove from empty
        self.assertIsNone(m.remove("any"))
        self.assertFalse(m.remove_value("any", 1))
        
        # Clear empty
        m.clear()  # Should not raise
        self.assertTrue(m.is_empty())
        
        # Compute on empty
        result = m.compute("a", lambda k, v: 1 if v is None else v)
        self.assertEqual(result, 1)
        self.assertEqual(m.get("a"), 1)

    def test_concurrent_modification(self):
        """Test that we can modify map during iteration safely."""
        m = KotMutableMap({"a": 1, "b": 2, "c": 3, "d": 4})
        
        # Get keys first to avoid RuntimeError
        keys_to_remove = [k for k, v in m.entries if v > 2]
        for key in keys_to_remove:
            m.remove(key)
        
        self.assertEqual(m.size, 2)
        self.assertFalse(m.contains_key("c"))
        self.assertFalse(m.contains_key("d"))


class TestKotMutableMapTypeSpecification(unittest.TestCase):
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
        
        # Test creating typed KotMutableMap with parent types
        animals_by_name = KotMutableMap[str, Animal]()
        self.assertEqual(len(animals_by_name), 0)
        
        # Add different subclass instances
        animals_by_name.put("Buddy", Dog("Buddy"))
        animals_by_name.put("Whiskers", Cat("Whiskers"))
        self.assertEqual(len(animals_by_name), 2)
        
        # Test with initial elements
        animals2 = KotMutableMap[str, Animal]([("Max", Dog("Max")), ("Luna", Cat("Luna"))])
        self.assertEqual(len(animals2), 2)
        self.assertIsInstance(animals2.get("Max"), Dog)
        self.assertIsInstance(animals2.get("Luna"), Cat)
        
        # Add more animals
        animals2.put("Rex", Dog("Rex"))
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
        
        # Test creating empty typed KotMutableMap
        animals_by_name = KotMutableMap.of_type(str, Animal)
        self.assertEqual(len(animals_by_name), 0)
        
        # Add different subclass instances
        animals_by_name.put("Buddy", Dog("Buddy"))
        animals_by_name.put("Whiskers", Cat("Whiskers"))
        self.assertEqual(len(animals_by_name), 2)
        
        # Test with initial elements (list of tuples)
        animals2 = KotMutableMap.of_type(str, Animal, [("Max", Dog("Max")), ("Luna", Cat("Luna"))])
        self.assertEqual(len(animals2), 2)
        self.assertIsInstance(animals2.get("Max"), Dog)
        self.assertIsInstance(animals2.get("Luna"), Cat)
        
        # Test with initial elements (dict)
        animals3 = KotMutableMap.of_type(str, Animal, {"Rex": Dog("Rex"), "Mittens": Cat("Mittens")})
        self.assertEqual(len(animals3), 2)
        self.assertIsInstance(animals3.get("Rex"), Dog)
        self.assertIsInstance(animals3.get("Mittens"), Cat)
        
        # Test type checking is enforced
        class NotAnimal:
            pass
        
        with self.assertRaises(TypeError):
            animals3.put("Invalid", NotAnimal())


if __name__ == '__main__':
    unittest.main()