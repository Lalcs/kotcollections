"""Test circular imports are properly handled."""
import unittest


class TestCircularImports(unittest.TestCase):
    """Test that circular imports between collection classes are handled correctly."""
    
    def test_import_all_modules(self):
        """Test that all modules can be imported without circular import errors."""
        # Import in different orders to test for circular dependencies
        from kotcollections import KotList, KotMutableList, KotSet, KotMutableSet, KotMap, KotMutableMap
        
        # Verify all classes are importable
        self.assertIsNotNone(KotList)
        self.assertIsNotNone(KotMutableList)
        self.assertIsNotNone(KotSet)
        self.assertIsNotNone(KotMutableSet)
        self.assertIsNotNone(KotMap)
        self.assertIsNotNone(KotMutableMap)
    
    def test_kot_list_methods_with_other_collections(self):
        """Test KotList methods that use other collection types."""
        from kotcollections import KotList, KotSet
        
        lst = KotList([1, 2, 3, 2, 1])
        
        # Test methods that return Python set
        unique_set = lst.to_set()
        self.assertIsInstance(unique_set, set)
        self.assertEqual(len(unique_set), 3)
        
        # Test methods that return KotSet
        kot_set = lst.to_kot_set()
        self.assertIsInstance(kot_set, KotSet)
        self.assertEqual(kot_set.size, 3)
        
        # Test methods that return KotMap
        grouped = lst.group_by(lambda x: x % 2)
        self.assertEqual(len(grouped), 2)
        # Values in group_by are KotList
        for key in grouped.keys:
            values = grouped.get(key)
            from kotcollections import KotList as KL
            self.assertIsInstance(values, KL)
        
        # Test methods that create KotMutableList
        mutable = lst.to_kot_mutable_list()
        self.assertEqual(mutable.size, 5)
    
    def test_kot_set_methods_with_other_collections(self):
        """Test KotSet methods that use other collection types."""
        from kotcollections import KotSet, KotList
        
        s = KotSet([1, 2, 3])
        
        # Test methods that return Python list
        lst = s.to_list()
        self.assertIsInstance(lst, list)
        self.assertEqual(len(lst), 3)
        
        # Test methods that return KotList
        kot_list = s.to_kot_list()
        self.assertIsInstance(kot_list, KotList)
        self.assertEqual(kot_list.size, 3)
        
        # Test methods that use KotList as input
        s2 = KotSet(KotList([2, 3, 4]))
        union = s.union(s2)
        self.assertEqual(union.size, 4)
        
        # Test union with KotList directly
        kot_lst = KotList([3, 4, 5])
        union2 = s.union(kot_lst)
        self.assertEqual(union2.size, 5)
        
        # Test methods that return KotMap
        grouped = s.group_by(lambda x: x % 2)
        self.assertEqual(len(grouped), 2)
        # Values in group_by are KotList (Kotlin-compatible)
        for key in grouped.keys:
            values = grouped.get(key)
            self.assertIsInstance(values, KotList)  # Kotlin-compatible: group_by returns List values
    
    def test_kot_map_with_other_collections(self):
        """Test KotMap methods with other collection types."""
        from kotcollections import KotMap, KotList, KotSet
        
        m = KotMap({1: 'a', 2: 'b', 3: 'c'})
        
        # Test methods that return KotList
        values_list = m.values  # values returns a KotList
        self.assertIsInstance(values_list, KotList)
        self.assertEqual(len(values_list), 3)
        
        # Test methods that return KotSet
        keys_set = m.keys  # keys returns a KotSet
        self.assertIsInstance(keys_set, KotSet)
        self.assertEqual(len(keys_set), 3)
        
        # Test entries property
        entries = m.entries  # entries returns a KotSet of tuples
        self.assertIsInstance(entries, KotSet)
        self.assertEqual(len(entries), 3)
        
        # Test to_list method
        pairs_list = m.to_list()
        self.assertIsInstance(pairs_list, list)
        self.assertEqual(len(pairs_list), 3)
    
    def test_cross_collection_operations(self):
        """Test operations that involve multiple collection types."""
        from kotcollections import KotList, KotSet, KotMap
        
        # Create collections
        lst = KotList([1, 2, 3, 2, 1])
        
        # Test to_set returns Python set
        python_set = lst.to_set()
        self.assertIsInstance(python_set, set)
        self.assertEqual(len(python_set), 3)
        
        # Test to_kot_set returns KotSet
        kot_set = lst.to_kot_set()
        self.assertIsInstance(kot_set, KotSet)
        self.assertEqual(kot_set.size, 3)
        
        # Test group_by returns KotMap with KotList values
        m = lst.group_by(lambda x: x)
        self.assertEqual(len(m), 3)
        
        # Convert back and forth between types
        lst2 = KotList(kot_set.to_list())  # from Python list
        self.assertEqual(lst2.size, 3)
        
        lst3 = kot_set.to_kot_list()  # direct conversion to KotList
        self.assertEqual(lst3.size, 3)
        
        # Use map values (should be KotList)
        for key in m.keys:
            values = m.get(key)
            self.assertIsInstance(values, KotList)
            # Test conversion of map values
            converted_set = values.to_set()  # Python set
            self.assertIsInstance(converted_set, set)
            kot_converted_set = values.to_kot_set()  # KotSet
            self.assertIsInstance(kot_converted_set, KotSet)
            self.assertEqual(kot_converted_set.size, len(converted_set))


if __name__ == '__main__':
    unittest.main()