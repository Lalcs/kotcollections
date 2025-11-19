#!/usr/bin/env python3
"""Test script to verify builtin types work correctly with typed collections."""

from kotcollections import KotList, KotMap, KotSet, KotMutableList, KotMutableMap, KotMutableSet

print("=" * 60)
print("Testing KotList with builtin types")
print("=" * 60)

# Test 1: KotList[str]
print("\n1. KotList[str] - Basic usage")
string_list = KotList[str](["hello", "world"])
print(f"   Created: {string_list}")
print(f"   Type: {type(string_list).__name__}")

# Test 2: Try to add wrong type
print("\n2. KotList[str] - Type checking")
mutable_strings = string_list.to_kot_mutable_list()
try:
    mutable_strings.add(123)  # Should fail
    print("   ❌ ERROR: Should have raised TypeError!")
except TypeError as e:
    print(f"   ✅ Correctly rejected int: {e}")

# Test 3: KotList[int]
print("\n3. KotList[int] - Basic usage")
int_list = KotList[int]([1, 2, 3, 4, 5])
print(f"   Created: {int_list}")
print(f"   Sum: {int_list.sum_of(lambda x: x)}")

# Test 4: Try to add wrong type to int list
print("\n4. KotList[int] - Type checking")
mutable_ints = int_list.to_kot_mutable_list()
try:
    mutable_ints.add("hello")  # Should fail
    print("   ❌ ERROR: Should have raised TypeError!")
except TypeError as e:
    print(f"   ✅ Correctly rejected str: {e}")

# Test 5: KotList[float]
print("\n5. KotList[float] - Basic usage")
float_list = KotList[float]([1.5, 2.7, 3.14])
print(f"   Created: {float_list}")
print(f"   Average: {float_list.average()}")

# Test 6: Empty typed list
print("\n6. Empty KotList[str]")
empty_strings = KotList[str]()
print(f"   Created empty: {empty_strings}")
empty_strings = empty_strings.to_kot_mutable_list()
empty_strings.add("first")
empty_strings.add("second")
print(f"   After adding: {empty_strings}")

print("\n" + "=" * 60)
print("Testing KotMap with builtin types")
print("=" * 60)

# Test 7: KotMap[str, int]
print("\n7. KotMap[str, int] - Basic usage")
scores = KotMap[str, int]([("Alice", 95), ("Bob", 87)])
print(f"   Created: {dict(scores.to_dict())}")

# Test 8: Try to add wrong value type
print("\n8. KotMap[str, int] - Value type checking")
mutable_scores = scores.to_kot_mutable_map()
try:
    mutable_scores.put("Charlie", "ninety")  # Should fail
    print("   ❌ ERROR: Should have raised TypeError!")
except TypeError as e:
    print(f"   ✅ Correctly rejected str value: {e}")

# Test 9: Try to add wrong key type
print("\n9. KotMap[str, int] - Key type checking")
try:
    mutable_scores.put(123, 90)  # Should fail
    print("   ❌ ERROR: Should have raised TypeError!")
except TypeError as e:
    print(f"   ✅ Correctly rejected int key: {e}")

# Test 10: KotMap[int, str]
print("\n10. KotMap[int, str] - Basic usage")
names = KotMap[int, str]({1: "one", 2: "two", 3: "three"})
print(f"   Created: {dict(names.to_dict())}")

print("\n" + "=" * 60)
print("Testing KotSet with builtin types")
print("=" * 60)

# Test 11: KotSet[str]
print("\n11. KotSet[str] - Basic usage")
tags = KotSet[str](["python", "kotlin", "java"])
print(f"   Created: {tags}")
print(f"   Size: {tags.size}")

# Test 12: Type checking in set
print("\n12. KotSet[str] - Type checking")
mutable_tags = tags.to_kot_mutable_set()
try:
    mutable_tags.add(42)  # Should fail
    print("   ❌ ERROR: Should have raised TypeError!")
except TypeError as e:
    print(f"   ✅ Correctly rejected int: {e}")

# Test 13: KotSet[int]
print("\n13. KotSet[int] - Basic usage")
numbers = KotSet[int]({1, 2, 3, 4, 5})
print(f"   Created: {numbers}")

# Test 14: Edge case - bool is subclass of int
print("\n14. Edge case: bool is subclass of int")
print(f"   isinstance(True, int): {isinstance(True, int)}")
print(f"   issubclass(bool, int): {issubclass(bool, int)}")
int_list_with_bool = KotList[int]([1, 2, 3])
mutable = int_list_with_bool.to_kot_mutable_list()
try:
    mutable.add(True)  # This might succeed since bool is subclass of int
    print(f"   ✅ Bool accepted in int list (bool is subclass of int): {mutable}")
except TypeError as e:
    print(f"   Bool rejected: {e}")

# Test 15: of_type method with builtins
print("\n15. of_type() method with builtins")
strings_via_of_type = KotList.of_type(str, ["a", "b", "c"])
print(f"   Created via of_type: {strings_via_of_type}")

# Test 16: Type preservation in conversions
print("\n16. Type preservation in conversions")
typed_list = KotList[str](["x", "y", "z"])
typed_set = typed_list.to_set()
print(f"   List: {typed_list}")
print(f"   Converted to set: {typed_set}")
print(f"   Set has _element_type: {hasattr(typed_set, '_element_type')}")
if hasattr(typed_set, '_element_type'):
    print(f"   Set element type: {typed_set._element_type}")

print("\n" + "=" * 60)
print("All builtin type tests completed!")
print("=" * 60)
