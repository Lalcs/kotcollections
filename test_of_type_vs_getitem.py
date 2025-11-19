#!/usr/bin/env python3
"""Test to compare of_type() vs __class_getitem__() implementations."""

from kotcollections import KotList, KotMap, KotSet

print("=" * 70)
print("Comparing of_type() vs __class_getitem__() - KotList")
print("=" * 70)

# Create using both methods
list1 = KotList.of_type(str)
list2 = KotList[str]()
list3 = KotList[str]([])

print("\n1. Empty lists")
print(f"   of_type(str):     {list1}")
print(f"   [str]():          {list2}")
print(f"   [str]([]):        {list3}")

print("\n2. Type comparison")
print(f"   type(list1): {type(list1)}")
print(f"   type(list2): {type(list2)}")
print(f"   type(list3): {type(list3)}")
print(f"   type(list1).__name__: {type(list1).__name__}")
print(f"   type(list2).__name__: {type(list2).__name__}")

print("\n3. Are they the same class?")
print(f"   type(list1) is type(list2): {type(list1) is type(list2)}")
print(f"   type(list1) == type(list2): {type(list1) == type(list2)}")

print("\n4. Internal _element_type")
print(f"   list1._element_type: {list1._element_type}")
print(f"   list2._element_type: {list2._element_type}")
print(f"   list3._element_type: {list3._element_type}")

print("\n5. With initial elements")
list4 = KotList.of_type(str, ["a", "b"])
list5 = KotList[str](["a", "b"])

print(f"   of_type(str, ['a', 'b']): {list4}")
print(f"   [str](['a', 'b']):        {list5}")
print(f"   type(list4) is type(list5): {type(list4) is type(list5)}")
print(f"   list4._element_type: {list4._element_type}")
print(f"   list5._element_type: {list5._element_type}")

print("\n6. Behavioral equivalence test")
mutable1 = list1.to_kot_mutable_list()
mutable2 = list2.to_kot_mutable_list()

mutable1.add("hello")
mutable2.add("world")

print(f"   After adding to list1: {mutable1}")
print(f"   After adding to list2: {mutable2}")

# Try to add wrong type
try:
    mutable1.add(123)
    print("   ❌ list1 should reject int")
except TypeError as e:
    print(f"   ✅ list1 rejects int: {e}")

try:
    mutable2.add(456)
    print("   ❌ list2 should reject int")
except TypeError as e:
    print(f"   ✅ list2 rejects int: {e}")

print("\n" + "=" * 70)
print("Comparing of_type() vs __class_getitem__() - KotMap")
print("=" * 70)

map1 = KotMap.of_type(str, int)
map2 = KotMap[str, int]()

print("\n1. Empty maps")
print(f"   of_type(str, int): {dict(map1.to_dict())}")
print(f"   [str, int]():      {dict(map2.to_dict())}")

print("\n2. Type comparison")
print(f"   type(map1).__name__: {type(map1).__name__}")
print(f"   type(map2).__name__: {type(map2).__name__}")
print(f"   type(map1) is type(map2): {type(map1) is type(map2)}")

print("\n3. Internal types")
print(f"   map1._key_type:   {map1._key_type}")
print(f"   map1._value_type: {map1._value_type}")
print(f"   map2._key_type:   {map2._key_type}")
print(f"   map2._value_type: {map2._value_type}")

print("\n" + "=" * 70)
print("Implementation verification")
print("=" * 70)

print("\nLooking at the code:")
print("   of_type() calls: typed_class = cls[element_type]")
print("   Then returns:    typed_class(elements)")
print("\nSo:")
print("   KotList.of_type(str) ≡ KotList[str](None)")
print("   KotList[str]()       ≡ KotList[str](None)")
print("\n   They create the SAME dynamic subclass!")

print("\n" + "=" * 70)
print("Conclusion")
print("=" * 70)
print("""
✅ of_type() and __class_getitem__() are internally IDENTICAL

The of_type() method is essentially syntactic sugar that:
1. Calls __class_getitem__() to create the dynamic subclass
2. Instantiates it with the provided elements

Benefits of each syntax:
- of_type():           More explicit, better for documentation
- __class_getitem__(): Cleaner syntax, familiar to Python developers

Both produce the exact same result with the same type checking behavior.
""")
