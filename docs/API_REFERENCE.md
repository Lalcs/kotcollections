# kotcollections API Reference

This document provides detailed information about all methods available in kotcollections. For basic usage and getting
started, please refer to the [README.md](../README.md).

## Table of Contents

- [KotList Methods](#kotlist-methods)
    - [Basic Properties and Access](#basic-properties-and-access)
    - [Search Methods](#search-methods)
    - [Transformation Methods](#transformation-methods)
    - [Filtering Methods](#filtering-methods)
    - [Testing Methods](#testing-methods)
    - [Aggregation Methods](#aggregation-methods)
    - [Sorting Methods](#sorting-methods)
    - [Grouping Methods](#grouping-methods)
    - [Collection Operations](#collection-operations)
    - [Other Operations](#other-operations)
    - [Conversion Methods](#conversion-methods)
- [KotMutableList Additional Methods](#kotmutablelist-additional-methods)
    - [Addition Methods](#addition-methods)
    - [Modification Methods](#modification-methods)
    - [In-place Sorting](#in-place-sorting)
- [KotSet Methods](#kotset-methods)
    - [Basic Usage](#kotset-basic-usage)
    - [Set Operations](#set-operations)
    - [Functional Operations](#functional-operations)
    - [Element Access](#element-access)
- [KotMutableSet Additional Methods](#kotmutableset-additional-methods)
    - [Basic Usage](#kotmutableset-basic-usage)
    - [Mutation Operations](#mutation-operations)
    - [Predicate-based Operations](#predicate-based-operations)
    - [In-place Set Operations](#in-place-set-operations)
    - [Conversion](#conversion)
- [KotMap Methods](#kotmap-methods)
    - [Basic Usage](#kotmap-basic-usage)
    - [Access Operations](#access-operations)
    - [Checking Operations](#checking-operations)
    - [Filtering Operations](#filtering-operations)
    - [Transformation Operations](#transformation-operations)
    - [Finding Operations](#finding-operations)
    - [Other Map Operations](#other-map-operations)
- [KotMutableMap Additional Methods](#kotmutablemap-additional-methods)
    - [Basic Usage](#kotmutablemap-basic-usage)
    - [Mutation Operations](#mutation-operations-map)
    - [Advanced Mutation Operations](#advanced-mutation-operations)

## KotList Methods

### Basic Properties and Access

#### size

Returns the number of elements in the list.

```python
lst = KotList([1, 2, 3])
print(lst.size)  # 3
```

#### is_empty() / is_not_empty()

Checks if the list is empty.

```python
lst = KotList([1, 2, 3])
print(lst.is_empty())  # False
print(lst.is_not_empty())  # True
```

#### indices / last_index

Gets the range of valid indices and the last index.

```python
lst = KotList([1, 2, 3])
print(lst.indices)  # range(0, 3)
print(lst.last_index)  # 2
```

#### get(index)

Gets the element at the specified index (throws exception if out of range).

```python
lst = KotList([10, 20, 30])
print(lst.get(1))  # 20
print(lst[1])  # 20 (same behavior)
```

#### get_or_null(index) / get_or_none(index)

Gets the element at the specified index (returns None if out of range). Both `get_or_null()` and `get_or_none()` can be
used.

```python
lst = KotList([10, 20, 30])
print(lst.get_or_null(1))  # 20
print(lst.get_or_null(10))  # None

# Using the Pythonic alias
print(lst.get_or_none(1))  # 20 (same as get_or_null)
print(lst.get_or_none(10))  # None
```

#### get_or_else(index, default_value)

Gets the element at the specified index (returns default value if out of range).

```python
lst = KotList([10, 20, 30])
print(lst.get_or_else(10, lambda i: i * 100))  # 1000
```

#### first() / last()

Gets the first/last element.

```python
lst = KotList([10, 20, 30])
print(lst.first())  # 10
print(lst.last())  # 30
```

#### first_or_null() / first_or_none() / last_or_null() / last_or_none()

Gets the first/last element (returns None if empty). Both `_null` and `_none` variants are available.

```python
lst = KotList([10, 20, 30])
print(lst.first_or_null())  # 10
print(lst.last_or_null())  # 30

empty = KotList()
print(empty.first_or_null())  # None
print(empty.first_or_none())  # None (Pythonic alias)
print(empty.last_or_none())  # None (Pythonic alias)
```

### Search Methods

#### contains(element)

Checks if an element is in the list.

```python
lst = KotList([1, 2, 3])
print(lst.contains(2))  # True
print(lst.contains(5))  # False
```

#### contains_all(elements)

Checks if all elements are in the list.

```python
lst = KotList([1, 2, 3, 4, 5])
print(lst.contains_all([2, 4]))  # True
print(lst.contains_all([2, 6]))  # False
```

#### index_of(element) / last_index_of(element)

Returns the first/last occurrence index (returns -1 if not found).

```python
lst = KotList([1, 2, 3, 2, 5])
print(lst.index_of(2))  # 1
print(lst.last_index_of(2))  # 3
print(lst.index_of(6))  # -1
```

#### index_of_first(predicate) / index_of_last(predicate)

Returns the index of the first/last element matching the predicate.

```python
lst = KotList([1, 2, 3, 4, 5])
print(lst.index_of_first(lambda x: x > 3))  # 3
print(lst.index_of_last(lambda x: x < 4))  # 2
```

#### binary_search(element, comparator=None)

Performs binary search on a sorted list.

```python
lst = KotList([1, 3, 5, 7, 9])
print(lst.binary_search(5))  # 2
print(lst.binary_search(4))  # -3 (negative insertion point - 1)
```

### Transformation Methods

#### map(transform)

Creates a new list with transformed elements.

```python
lst = KotList([1, 2, 3])
doubled = lst.map(lambda x: x * 2)
print(doubled.to_list())  # [2, 4, 6]
```

#### map_indexed(transform)

Transforms each element with its index.

```python
lst = KotList(['a', 'b', 'c'])
indexed = lst.map_indexed(lambda i, x: f"{i}:{x}")
print(indexed.to_list())  # ['0:a', '1:b', '2:c']
```

#### map_not_null(transform) / map_not_none(transform)

Creates a new list containing only non-None transformation results. Both `map_not_null()` and `map_not_none()` can be
used.

```python
lst = KotList([1, 2, 3, 4])
evens = lst.map_not_null(lambda x: x * 2 if x % 2 == 0 else None)
print(evens.to_list())  # [4, 8]
```

#### flat_map(transform)

Transforms each element to multiple elements and flattens the result.

```python
lst = KotList([1, 2, 3])
expanded = lst.flat_map(lambda x: [x, x * 10])
print(expanded.to_list())  # [1, 10, 2, 20, 3, 30]
```

#### flatten()

Flattens nested lists.

```python
lst = KotList([[1, 2], [3, 4], [5]])
flattened = lst.flatten()
print(flattened.to_list())  # [1, 2, 3, 4, 5]
```

#### associate_with(value_selector)

Creates a KotMap with elements as keys.

```python
lst = KotList(['a', 'bb', 'ccc'])
length_map = lst.associate_with(lambda x: len(x))
print(length_map.to_dict())  # {'a': 1, 'bb': 2, 'ccc': 3}

# Use as KotMap
print(length_map.get('bb'))  # 2
print(length_map.contains_key('a'))  # True
print(list(length_map.keys()))  # ['a', 'bb', 'ccc']
```

#### associate_by(key_selector)

Creates a KotMap with keys generated from elements.

```python
lst = KotList(['a', 'bb', 'ccc'])
by_length = lst.associate_by(lambda x: len(x))
print(by_length.to_dict())  # {1: 'a', 2: 'bb', 3: 'ccc'}

# Use as KotMap
print(by_length.get(2))  # 'bb'
print(by_length.contains_key(1))  # True
print(list(by_length.values()))  # ['a', 'bb', 'ccc']
```

### Filtering Methods

#### filter(predicate)

Creates a new list containing only elements matching the predicate.

```python
lst = KotList([1, 2, 3, 4, 5])
evens = lst.filter(lambda x: x % 2 == 0)
print(evens.to_list())  # [2, 4]
```

#### filter_indexed(predicate)

Filters using both index and element.

```python
lst = KotList(['a', 'b', 'c', 'd'])
even_indices = lst.filter_indexed(lambda i, x: i % 2 == 0)
print(even_indices.to_list())  # ['a', 'c']
```

#### filter_not(predicate)

Creates a new list containing elements not matching the predicate.

```python
lst = KotList([1, 2, 3, 4, 5])
odds = lst.filter_not(lambda x: x % 2 == 0)
print(odds.to_list())  # [1, 3, 5]
```

#### filter_not_null() / filter_not_none()

Creates a new list containing only non-None elements. Both `filter_not_null()` and `filter_not_none()` can be used.

```python
lst = KotList([1, None, 2, None, 3])
non_nulls = lst.filter_not_null()
print(non_nulls.to_list())  # [1, 2, 3]

# Using the Pythonic alias
non_nones = lst.filter_not_none()
print(non_nones.to_list())  # [1, 2, 3]
```

#### filter_is_instance(klass)

Creates a new list containing only elements of the specified type.

```python
lst = KotList([1, 'a', 2, 'b', 3.0])
integers = lst.filter_is_instance(int)
print(integers.to_list())  # [1, 2]
```

#### partition(predicate)

Splits into elements matching and not matching the predicate.

```python
lst = KotList([1, 2, 3, 4, 5])
evens, odds = lst.partition(lambda x: x % 2 == 0)
print(evens.to_list())  # [2, 4]
print(odds.to_list())  # [1, 3, 5]
```

### Testing Methods

#### any(predicate=None)

Checks if any element matches the condition.

```python
lst = KotList([1, 2, 3, 4, 5])
print(lst.any(lambda x: x > 3))  # True
print(lst.any(lambda x: x > 10))  # False
print(lst.any())  # True (checks if list has elements)
```

#### all(predicate)

Checks if all elements match the condition.

```python
lst = KotList([2, 4, 6, 8])
print(lst.all(lambda x: x % 2 == 0))  # True
```

#### none(predicate=None)

Checks if no elements match the condition.

```python
lst = KotList([1, 2, 3])
print(lst.none(lambda x: x > 10))  # True
print(lst.none())  # False (checks if list is empty)
```

### Aggregation Methods

#### count(predicate=None)

Returns the number of elements or elements matching the predicate.

```python
lst = KotList([1, 2, 3, 4, 5])
print(lst.count())  # 5
print(lst.count(lambda x: x % 2 == 0))  # 2
```

#### sum_of(selector)

Calculates the sum of transformed elements.

```python
lst = KotList([1, 2, 3, 4, 5])
print(lst.sum_of(lambda x: x))  # 15
print(lst.sum_of(lambda x: x * 2))  # 30
```

#### max_or_null() / max_or_none() / min_or_null() / min_or_none()

Returns the maximum/minimum value (None if empty). Both `_null` and `_none` variants are available.

```python
lst = KotList([3, 1, 4, 1, 5])
print(lst.max_or_null())  # 5
print(lst.min_or_null())  # 1
```

#### max_by_or_null(selector) / max_by_or_none(selector) / min_by_or_null(selector) / min_by_or_none(selector)

Returns the element with the maximum/minimum selector result. Both `_null` and `_none` variants are available.

```python
lst = KotList(['a', 'bbb', 'cc'])
print(lst.max_by_or_null(lambda x: len(x)))  # 'bbb'
print(lst.min_by_or_null(lambda x: len(x)))  # 'a'
```

#### average()

Calculates the average of numeric list.

```python
lst = KotList([1, 2, 3, 4, 5])
print(lst.average())  # 3.0
```

### Sorting Methods

#### sorted(key=None, reverse=False)

Returns a new sorted list.

```python
lst = KotList([3, 1, 4, 1, 5])
sorted_asc = lst.sorted()
print(sorted_asc.to_list())  # [1, 1, 3, 4, 5]

sorted_desc = lst.sorted(reverse=True)
print(sorted_desc.to_list())  # [5, 4, 3, 1, 1]
```

#### sorted_by(selector) / sorted_by_descending(selector)

Sorts by selector result.

```python
lst = KotList(['bb', 'aaa', 'c'])
by_length = lst.sorted_by(lambda x: len(x))
print(by_length.to_list())  # ['c', 'bb', 'aaa']
```

#### reversed()

Returns a new reversed list.

```python
lst = KotList([1, 2, 3, 4, 5])
reversed_lst = lst.reversed()
print(reversed_lst.to_list())  # [5, 4, 3, 2, 1]
```

#### shuffled(random_instance=None)

Returns a new shuffled list.

```python
import random

lst = KotList([1, 2, 3, 4, 5])
rng = random.Random(42)  # Reproducible shuffle
shuffled = lst.shuffled(rng)
print(shuffled.to_list())  # Shuffled elements
```

### Grouping Methods

#### group_by(key_selector)

Groups elements by key, returning a KotMap where values are KotList instances.

```python
lst = KotList([1, 2, 3, 4, 5, 6])
by_parity = lst.group_by(lambda x: x % 2)

# Access using KotMap methods
print(by_parity.get(0).to_list())  # [2, 4, 6]
print(by_parity.get(1).to_list())  # [1, 3, 5]

# Other KotMap operations
print(by_parity.contains_key(0))  # True
print(list(by_parity.keys()))  # [0, 1]

# Values are KotList instances
for key, group in by_parity.entries():
    print(f"Key {key}: {group.to_list()}")
```

#### chunked(size)

Splits into chunks of specified size.

```python
lst = KotList([1, 2, 3, 4, 5, 6, 7])
chunks = lst.chunked(3)
print(chunks[0].to_list())  # [1, 2, 3]
print(chunks[1].to_list())  # [4, 5, 6]
print(chunks[2].to_list())  # [7]
```

#### windowed(size, step=1, partial_windows=False)

Creates sliding windows.

```python
lst = KotList([1, 2, 3, 4, 5])
windows = lst.windowed(3)
print(windows[0].to_list())  # [1, 2, 3]
print(windows[1].to_list())  # [2, 3, 4]
print(windows[2].to_list())  # [3, 4, 5]

# With step
windows_step = lst.windowed(3, step=2)
print(windows_step[0].to_list())  # [1, 2, 3]
print(windows_step[1].to_list())  # [3, 4, 5]
```

### Collection Operations

#### distinct()

Returns a new list without duplicates.

```python
lst = KotList([1, 2, 2, 3, 3, 3])
unique = lst.distinct()
print(unique.to_list())  # [1, 2, 3]
```

#### distinct_by(selector)

Removes duplicates based on selector result.

```python
lst = KotList(['a', 'aa', 'b', 'bb', 'ccc'])
by_length = lst.distinct_by(lambda x: len(x))
print(by_length.to_list())  # ['a', 'aa', 'ccc']
```

#### intersect(other)

Returns the intersection of two lists.

```python
lst1 = KotList([1, 2, 3, 4, 5])
lst2 = [3, 4, 5, 6, 7]
common = lst1.intersect(lst2)
print(common.to_list())  # [3, 4, 5]
```

#### union(other)

Returns the union of two lists.

```python
lst1 = KotList([1, 2, 3])
lst2 = [3, 4, 5]
combined = lst1.union(lst2)
print(combined.to_list())  # [1, 2, 3, 4, 5]
```

#### plus(element) / minus(element)

Returns a new list with element added/removed.

```python
lst = KotList([1, 2, 3])

# Add element
plus_one = lst.plus(4)
print(plus_one.to_list())  # [1, 2, 3, 4]

# Add multiple elements
plus_many = lst.plus([4, 5])
print(plus_many.to_list())  # [1, 2, 3, 4, 5]

# Remove element
minus_one = lst.minus(2)
print(minus_one.to_list())  # [1, 3]
```

#### subtract(other)

Returns a list containing all elements of the original list except the elements contained in the given other collection.

```python
lst1 = KotList([1, 2, 3, 4, 5])
lst2 = [2, 4, 6]
result = lst1.subtract(lst2)
print(result.to_list())  # [1, 3, 5]

# Works with KotSet and KotMap too
from kotcollections import KotSet, KotMap
kot_set = KotSet([1, 3])
result2 = lst1.subtract(kot_set)
print(result2.to_list())  # [2, 4, 5]

kot_map = KotMap({"a": 2, "b": 4})
result3 = lst1.subtract(kot_map)  # Subtracts map values
print(result3.to_list())  # [1, 3, 5]
```

#### slice_range(indices)

Returns a list containing elements at specified range of indices.

```python
lst = KotList([10, 20, 30, 40, 50])

# Basic range
result = lst.slice_range(range(1, 4))
print(result.to_list())  # [20, 30, 40]

# With step
result_step = lst.slice_range(range(0, 5, 2))
print(result_step.to_list())  # [10, 30, 50]

# Empty range
result_empty = lst.slice_range(range(0, 0))
print(result_empty.to_list())  # []
```

#### sub_list(from_index, to_index)

Returns a sublist.

```python
lst = KotList([1, 2, 3, 4, 5])
sub = lst.sub_list(1, 4)
print(sub.to_list())  # [2, 3, 4]
```

### Other Operations

#### zip(other) / unzip()

Pairs two lists / unpairs a list of pairs.

```python
lst1 = KotList([1, 2, 3])
lst2 = ['a', 'b', 'c']
zipped = lst1.zip(lst2)
print(zipped.to_list())  # [(1, 'a'), (2, 'b'), (3, 'c')]

# Unzip
pairs = KotList([(1, 'a'), (2, 'b'), (3, 'c')])
numbers, letters = pairs.unzip()
print(numbers.to_list())  # [1, 2, 3]
print(letters.to_list())  # ['a', 'b', 'c']
```

#### fold(initial, operation) / reduce(operation)

Processes elements sequentially to produce a single value.

```python
lst = KotList([1, 2, 3, 4])

# fold (with initial value)
sum_fold = lst.fold(0, lambda acc, x: acc + x)
print(sum_fold)  # 10

# reduce (without initial value)
sum_reduce = lst.reduce(lambda a, b: a + b)
print(sum_reduce)  # 10
```

#### scan(initial, operation)

Returns a list of cumulative values.

```python
lst = KotList([1, 2, 3, 4])
cumulative = lst.scan(0, lambda acc, x: acc + x)
print(cumulative.to_list())  # [0, 1, 3, 6, 10]
```

#### for_each(action) / for_each_indexed(action)

Performs an action on each element.

```python
lst = KotList([1, 2, 3])

# Print each element
lst.for_each(lambda x: print(x))

# Print with index
lst.for_each_indexed(lambda i, x: print(f"{i}: {x}"))
```

#### on_each(action)

Performs an action on each element and returns the original list (for method chaining).

```python
lst = KotList([1, 2, 3])
result = lst.on_each(lambda x: print(x)).map(lambda x: x * 2)
```

#### join_to_string(separator=", ", prefix="", postfix="", limit=-1, truncated="...", transform=None)

Joins elements into a string.

```python
lst = KotList([1, 2, 3])

# Basic join
print(lst.join_to_string())  # "1, 2, 3"

# Custom format
print(
    lst.join_to_string(
        separator=" | ",
        prefix="[",
        postfix="]"
    )
)  # "[1 | 2 | 3]"

# With limit and transform
lst_long = KotList(range(10))
print(
    lst_long.join_to_string(
        limit=3,
        truncated="...",
        transform=lambda x: f"n{x}"
    )
)  # "n0, n1, n2..."
```

### Conversion Methods

#### to_list()

Converts to a Python standard list.

```python
kot_list = KotList([1, 2, 3])
py_list = kot_list.to_list()
print(type(py_list))  # <class 'list'>
```

#### to_mutable_list()

Converts to KotMutableList.

```python
kot_list = KotList([1, 2, 3])
mutable = kot_list.to_mutable_list()
mutable.add(4)
print(mutable.to_list())  # [1, 2, 3, 4]
```

#### to_set() / to_mutable_set()

Converts to Python set or KotMutableSet.

```python
lst = KotList([1, 2, 2, 3, 3])
unique_set = lst.to_set()
print(unique_set)  # {1, 2, 3}

# Convert to KotMutableSet
mutable_set = lst.to_mutable_set()
print(type(mutable_set))  # <class 'kotcollections.kot_mutable_set.KotMutableSet'>
```

## KotMutableList Additional Methods

KotMutableList provides all KotList methods plus the following modification methods:

### Addition Methods

#### add(element)

Adds an element to the end of the list.

```python
lst = KotMutableList([1, 2, 3])
lst.add(4)
print(lst.to_list())  # [1, 2, 3, 4]
```

#### add_at(index, element)

Inserts an element at the specified position.

```python
lst = KotMutableList([1, 3])
lst.add_at(1, 2)
print(lst.to_list())  # [1, 2, 3]
```

#### add_all(elements) / add_all_at(index, elements)

Adds multiple elements.

```python
lst = KotMutableList([1, 2])
lst.add_all([3, 4, 5])
print(lst.to_list())  # [1, 2, 3, 4, 5]

lst.add_all_at(2, [2.5, 2.7])
print(lst.to_list())  # [1, 2, 2.5, 2.7, 3, 4, 5]
```

### Modification Methods

#### set(index, element)

Replaces the element at the specified position.

```python
lst = KotMutableList([1, 2, 3])
old = lst.set(1, 10)
print(old)  # 2
print(lst.to_list())  # [1, 10, 3]
```

#### remove_at(index)

Removes the element at the specified position.

```python
lst = KotMutableList([1, 2, 3])
removed = lst.remove_at(1)
print(removed)  # 2
print(lst.to_list())  # [1, 3]
```

#### remove(element)

Removes the first occurrence of the element.

```python
lst = KotMutableList([1, 2, 3, 2])
lst.remove(2)
print(lst.to_list())  # [1, 3, 2]
```

#### remove_all(elements)

Removes all specified elements.

```python
lst = KotMutableList([1, 2, 3, 2, 4])
lst.remove_all([2, 4])
print(lst.to_list())  # [1, 3]
```

#### retain_all(elements)

Keeps only the specified elements.

```python
lst = KotMutableList([1, 2, 3, 4, 5])
lst.retain_all([2, 4, 6])
print(lst.to_list())  # [2, 4]
```

#### clear()

Removes all elements.

```python
lst = KotMutableList([1, 2, 3])
lst.clear()
print(lst.to_list())  # []
```

#### remove_if(predicate)

Removes all elements that satisfy the given predicate. Returns true if any elements were removed.

```python
lst = KotMutableList([1, 2, 3, 4, 5, 6])

# Remove even numbers
result = lst.remove_if(lambda x: x % 2 == 0)
print(result)  # True (elements were removed)
print(lst.to_list())  # [1, 3, 5]

# Try to remove numbers > 10 (none exist)
result = lst.remove_if(lambda x: x > 10)
print(result)  # False (no elements were removed)
print(lst.to_list())  # [1, 3, 5] (unchanged)
```

#### replace_all(operator)

Replaces each element of this list with the result of applying the operator to that element.

```python
lst = KotMutableList([1, 2, 3, 4, 5])

# Double all elements
lst.replace_all(lambda x: x * 2)
print(lst.to_list())  # [2, 4, 6, 8, 10]

# Square all elements
lst.replace_all(lambda x: x ** 2)
print(lst.to_list())  # [4, 16, 36, 64, 100]

# With strings
str_lst = KotMutableList(['hello', 'world', 'test'])
str_lst.replace_all(lambda s: s.upper())
print(str_lst.to_list())  # ['HELLO', 'WORLD', 'TEST']
```

### In-place Sorting

#### sort(key=None, reverse=False)

Sorts the list in place.

```python
lst = KotMutableList([3, 1, 4, 1, 5])
lst.sort()
print(lst.to_list())  # [1, 1, 3, 4, 5]
```

#### sort_by(selector) / sort_by_descending(selector)

Sorts by selector result.

```python
lst = KotMutableList(['bb', 'aaa', 'c'])
lst.sort_by(lambda x: len(x))
print(lst.to_list())  # ['c', 'bb', 'aaa']
```

#### reverse()

Reverses the list in place.

```python
lst = KotMutableList([1, 2, 3])
lst.reverse()
print(lst.to_list())  # [3, 2, 1]
```

#### shuffle(random_instance=None)

Shuffles the list in place.

```python
lst = KotMutableList([1, 2, 3, 4, 5])
lst.shuffle()
# Elements are randomly rearranged
```

#### fill(value)

Replaces all elements with the specified value.

```python
lst = KotMutableList([1, 2, 3])
lst.fill(0)
print(lst.to_list())  # [0, 0, 0]
```

## KotSet Methods

KotSet is a Python implementation of Kotlin's Set interface, providing a read-only set with rich functional operations.

### Basic Usage {#kotset-basic-usage}

```python
from kotcollections import KotSet

# Create from various sources
s1 = KotSet([1, 2, 3, 3, 2, 1])  # Duplicates removed: {1, 2, 3}
s2 = KotSet({4, 5, 6})  # From Python set
s3 = KotSet()  # Empty set

# Type safety
numbers = KotSet([1, 2, 3])  # KotSet[int]
# mixed = KotSet([1, "2", 3])  # TypeError!
```

### Set Operations

```python
set1 = KotSet([1, 2, 3])
set2 = KotSet([3, 4, 5])

# Union
union = set1.union(set2)  # {1, 2, 3, 4, 5}

# Intersection
intersection = set1.intersect(set2)  # {3}

# Difference
difference = set1.subtract(set2)  # {1, 2}
```

### Functional Operations

```python
s = KotSet([1, 2, 3, 4, 5])

# Transformation
doubled = s.map(lambda x: x * 2)  # {2, 4, 6, 8, 10}
evens = s.filter(lambda x: x % 2 == 0)  # {2, 4}

# Aggregation
sum_result = s.sum_of(lambda x: x)  # 15
avg_result = s.average(lambda x: x)  # 3.0
max_result = s.max_or_none()  # 5

# Grouping
grouped = s.group_by(lambda x: x % 2)  # Returns KotMap with KotSet values
print(grouped.get(0))  # KotSet([2, 4])
print(grouped.get(1))  # KotSet([1, 3, 5])

# Group and transform values
grouped_lengths = s.group_by_to(
    lambda x: x % 2,  # Group by parity
    lambda x: x * x  # Transform to squares
)
print(grouped_lengths.get(0).to_list())  # [4, 16] (squares of even numbers)
print(grouped_lengths.get(1).to_list())  # [1, 9, 25] (squares of odd numbers)
```

### Transformation Methods

#### associate(transform)

Returns a KotMap containing key-value pairs provided by transform function.

```python
s = KotSet([1, 2, 3])
pairs = s.associate(lambda x: (x, x * x))
print(pairs.to_dict())  # {1: 1, 2: 4, 3: 9}

# Use as KotMap
print(pairs.get(2))  # 4
print(pairs.contains_key(3))  # True
```

#### associate_by(key_selector)

Returns a KotMap with keys generated by key_selector and values from elements.

```python
s = KotSet(["hello", "world", "test"])
by_length = s.associate_by(len)
print(by_length.get(4))  # "test"
print(by_length.get(5))  # "hello" or "world" (order not guaranteed in sets)

# Use as KotMap
print(set(by_length.keys))  # {4, 5}
```

#### associate_with(value_selector)

Returns a KotMap where keys are elements and values are produced by value_selector.

```python
s = KotSet(["apple", "banana", "cherry"])
length_map = s.associate_with(len)
print(length_map.to_dict())  # {'apple': 5, 'banana': 6, 'cherry': 6}

# Use as KotMap
print(length_map.get("apple"))  # 5
print(list(length_map.values))  # [5, 6, 6] (order may vary)
```

### Element Access

```python
s = KotSet([1, 2, 3])

# Safe access methods
first = s.first_or_none()  # Returns an element (order not guaranteed)
single = s.single_or_none()  # None (more than one element)

# Checking elements
contains = s.contains(2)  # True
contains_all = s.contains_all([1, 2])  # True
```

## KotMutableSet Additional Methods

KotMutableSet extends KotSet with mutation methods, providing a mutable set implementation.

### Basic Usage {#kotmutableset-basic-usage}

```python
from kotcollections import KotMutableSet

# Create mutable set
ms = KotMutableSet([1, 2, 3])

# Add elements
ms.add(4)  # Returns True (element added)
ms.add(3)  # Returns False (element already exists)

# Add multiple elements
ms.add_all([5, 6, 7])  # Returns True if any added
```

### Mutation Operations

```python
ms = KotMutableSet([1, 2, 3, 4, 5])

# Remove elements
ms.remove(3)  # Returns True (element removed)
ms.remove_all([1, 2])  # Returns True if any removed

# Retain elements
ms.retain_all([4, 5, 6])  # Keeps only specified elements

# Clear all
ms.clear()  # Empties the set
```

### Predicate-based Operations

```python
ms = KotMutableSet([1, 2, 3, 4, 5, 6])

# Remove with predicate
ms.remove_if(lambda x: x % 2 == 0)  # Removes even numbers

# Retain with predicate
ms2 = KotMutableSet([1, 2, 3, 4, 5, 6])
ms2.retain_if(lambda x: x > 3)  # Keeps only elements > 3
```

### In-place Set Operations

```python
ms1 = KotMutableSet([1, 2, 3])
ms2 = KotSet([3, 4, 5])

# In-place operations
ms1.union_update(ms2)  # ms1 becomes {1, 2, 3, 4, 5}
ms1.intersect_update(ms2)  # ms1 becomes {3, 4, 5}
ms1.subtract_update(ms2)  # ms1 becomes empty

# Operator shortcuts
ms1 += ms2  # union_update
ms1 -= ms2  # subtract_update
ms1 &= ms2  # intersect_update
```

### Conversion

```python
# Convert to immutable
mutable_set = KotMutableSet([1, 2, 3])
immutable_set = mutable_set.to_set()  # Returns KotSet

# Convert to Python types
python_set = mutable_set.to_set()  # Returns set
python_list = mutable_set.to_list()  # Returns list
sorted_list = mutable_set.to_sorted_list()  # Returns sorted list
```

## KotMap Methods

KotMap is a Python implementation of Kotlin's Map interface, providing a read-only map with rich functional operations.

### Basic Usage {#kotmap-basic-usage}

```python
from kotcollections import KotMap

# Create from various sources
m1 = KotMap({"a": 1, "b": 2, "c": 3})  # From dict
m2 = KotMap([("a", 1), ("b", 2), ("c", 3)])  # From list of tuples
m3 = KotMap()  # Empty map

# Type safety
numbers_map = KotMap({"one": 1, "two": 2})  # KotMap[str, int]
# mixed = KotMap({"one": 1, "two": "2"})  # TypeError!
```

### Access Operations

#### get(key) / get_or_null(key) / get_or_none(key)

Returns the value corresponding to the given key, or None if not present.

```python
m = KotMap({"a": 1, "b": 2, "c": 3})

print(m.get("b"))  # 2
print(m.get("d"))  # None
print(m.get_or_null("d"))  # None
print(m.get_or_none("d"))  # None (Pythonic alias)
```

#### get_or_default(key, default_value)

Returns the value corresponding to the given key, or default_value if not present.

```python
m = KotMap({"a": 1, "b": 2})
print(m.get_or_default("c", 99))  # 99
```

#### get_or_else(key, default_value)

Returns the value for the given key. If not found, calls the defaultValue function.

```python
m = KotMap({"a": 1, "b": 2})
print(m.get_or_else("c", lambda: 3 * 3))  # 9
```

#### get_value(key)

Returns the value for the given key or throws an exception if the key is missing.

```python
m = KotMap({"a": 1, "b": 2})
print(m.get_value("a"))  # 1
# m.get_value("c")  # Raises KeyError
```

#### keys / values / entries

Access the map's keys, values, and entries.

```python
m = KotMap({"a": 1, "b": 2, "c": 3})

print(m.keys)  # {a, b, c}
print(m.values)  # [1, 2, 3]
print(m.entries)  # {('a', 1), ('b', 2), ('c', 3)}
```

#### contains_key(key) / contains_value(value)

Check if the map contains a key or value.

```python
m = KotMap({"a": 1, "b": 2, "c": 3})

print(m.contains_key("b"))  # True
print(m.contains_value(2))  # True
print(m.contains_key("d"))  # False
```

### Checking Operations

#### all(predicate) / any(predicate) / none(predicate)

Check if all/any/no entries match the given predicate.

```python
m = KotMap({"a": 1, "b": 2, "c": 3})

print(m.all(lambda k, v: v > 0))  # True
print(m.any(lambda k, v: v > 2))  # True
print(m.none(lambda k, v: v > 5))  # True
```

#### count(predicate=None)

Returns the number of entries matching the given predicate.

```python
m = KotMap({"a": 1, "b": 2, "c": 3, "d": 4})

print(m.count())  # 4
print(m.count(lambda k, v: v % 2 == 0))  # 2
```

### Filtering Operations

#### filter(predicate)

Returns a map containing only entries matching the given predicate.

```python
m = KotMap({"a": 1, "b": 2, "c": 3, "d": 4})
evens = m.filter(lambda k, v: v % 2 == 0)
print(evens.to_dict())  # {'b': 2, 'd': 4}
```

#### filter_not(predicate)

Returns a map containing only entries not matching the predicate.

```python
m = KotMap({"a": 1, "b": 2, "c": 3, "d": 4})
odds = m.filter_not(lambda k, v: v % 2 == 0)
print(odds.to_dict())  # {'a': 1, 'c': 3}
```

#### filter_keys(predicate) / filter_values(predicate)

Filter by keys or values only.

```python
m = KotMap({"apple": 1, "banana": 2, "cherry": 3})

# Filter by keys starting with 'a'
a_fruits = m.filter_keys(lambda k: k.startswith('a'))
print(a_fruits.to_dict())  # {'apple': 1}

# Filter by values greater than 1
gt_one = m.filter_values(lambda v: v > 1)
print(gt_one.to_dict())  # {'banana': 2, 'cherry': 3}
```

#### filter_not_null() / filter_not_none()

Returns a map containing only entries with non-null values.

```python
m = KotMap({"a": 1, "b": None, "c": 3, "d": None})
non_nulls = m.filter_not_null()
print(non_nulls.to_dict())  # {'a': 1, 'c': 3}
```

### Transformation Operations

#### map(transform)

Returns a list containing the results of applying the transform function to each entry.

```python
m = KotMap({"a": 1, "b": 2, "c": 3})
results = m.map(lambda k, v: f"{k}:{v}")
print(results)  # ['a:1', 'b:2', 'c:3']
```

#### map_keys(transform) / map_values(transform)

Transform keys or values to create a new map.

```python
m = KotMap({"a": 1, "b": 2, "c": 3})

# Transform keys to uppercase
upper_keys = m.map_keys(lambda k, v: k.upper())
print(upper_keys.to_dict())  # {'A': 1, 'B': 2, 'C': 3}

# Transform values to squares
squares = m.map_values(lambda k, v: v * v)
print(squares.to_dict())  # {'a': 1, 'b': 4, 'c': 9}
```

#### map_not_null(transform) / map_not_none(transform)

Returns a list containing only non-null transformation results.

```python
m = KotMap({"a": 1, "b": 2, "c": 3, "d": 4})
evens_doubled = m.map_not_null(lambda k, v: v * 2 if v % 2 == 0 else None)
print(evens_doubled)  # [4, 8]
```

#### flat_map(transform)

Returns a single list of all elements yielded from results of transform function.

```python
m = KotMap({"a": 1, "b": 2})
expanded = m.flat_map(lambda k, v: [k, str(v)])
print(expanded)  # ['a', '1', 'b', '2']
```

### Finding Operations

#### max_by_or_null(selector) / max_by_or_none(selector)

Returns the entry yielding the largest value of the given function.

```python
m = KotMap({"a": 10, "b": 30, "c": 20})
max_entry = m.max_by_or_null(lambda k, v: v)
print(max_entry)  # ('b', 30)
```

#### min_by_or_null(selector) / min_by_or_none(selector)

Returns the entry yielding the smallest value of the given function.

```python
m = KotMap({"a": 10, "b": 30, "c": 20})
min_entry = m.min_by_or_null(lambda k, v: v)
print(min_entry)  # ('a', 10)
```

### Other Map Operations

#### plus(other) / minus(keys)

Create new maps with entries added or removed.

```python
m1 = KotMap({"a": 1, "b": 2})
m2 = KotMap({"c": 3, "d": 4})

# Combine maps
combined = m1.plus(m2)
print(combined.to_dict())  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Add single entry
with_e = combined.plus(("e", 5))
print(with_e.to_dict())  # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

# Remove keys
without_b = combined.minus("b")
print(without_b.to_dict())  # {'a': 1, 'c': 3, 'd': 4}

# Remove multiple keys
without_ac = combined.minus(["a", "c"])
print(without_ac.to_dict())  # {'b': 2, 'd': 4}
```

#### with_default(default_value)

Returns a wrapper providing a default value for missing keys.

```python
m = KotMap({"a": 1, "b": 2})
with_default = m.with_default(lambda k: len(k))

print(with_default.get("a"))  # 1
print(with_default.get("missing"))  # 7 (length of "missing")
```

#### for_each(action) / on_each(action)

Perform actions on each entry.

```python
m = KotMap({"a": 1, "b": 2, "c": 3})

# Print each entry
m.for_each(lambda k, v: print(f"{k} -> {v}"))

# Chain operations
result = m.on_each(lambda k, v: print(f"Processing {k}")).filter(lambda k, v: v > 1)
```

#### join_to_string(separator=", ", prefix="", postfix="", limit=-1, truncated="...", transform=None)

Creates a string from all entries.

```python
m = KotMap({"a": 1, "b": 2, "c": 3})

# Basic join
print(m.join_to_string())  # "a=1, b=2, c=3"

# Custom format
print(
    m.join_to_string(
        separator=" | ",
        prefix="{",
        postfix="}",
        transform=lambda k, v: f"{k}:{v}"
    )
)  # "{a:1 | b:2 | c:3}"
```

#### to_list() / to_dict()

Convert to Python types.

```python
m = KotMap({"a": 1, "b": 2, "c": 3})

pairs = m.to_list()  # [('a', 1), ('b', 2), ('c', 3)]
dict_copy = m.to_dict()  # {'a': 1, 'b': 2, 'c': 3}
```

## KotMutableMap Additional Methods

KotMutableMap extends KotMap with mutation methods, providing a mutable map implementation.

### Basic Usage {#kotmutablemap-basic-usage}

```python
from kotcollections import KotMutableMap

# Create mutable map
mm = KotMutableMap({"a": 1, "b": 2, "c": 3})

# Add/update entries
mm.put("d", 4)
mm["e"] = 5  # Using [] operator

# Remove entries
mm.remove("a")
del mm["b"]  # Using del operator
```

### Mutation Operations {#mutation-operations-map}

#### put(key, value)

Associates the specified value with the specified key in the map.

```python
mm = KotMutableMap({"a": 1})
old_value = mm.put("a", 10)  # Returns 1 (old value)
new_value = mm.put("b", 2)  # Returns None (new key)
```

#### put_all(from_map)

Updates this map with key/value pairs from the specified map.

```python
mm = KotMutableMap({"a": 1, "b": 2})
mm.put_all({"c": 3, "d": 4})
print(mm.to_dict())  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

#### put_if_absent(key, value)

Associates the value with the key only if it is not already associated.

```python
mm = KotMutableMap({"a": 1})
result1 = mm.put_if_absent("a", 10)  # Returns 1 (existing value)
result2 = mm.put_if_absent("b", 2)  # Returns None (added)
print(mm.to_dict())  # {'a': 1, 'b': 2}
```

#### remove(key) / remove_value(key, value)

Remove entries from the map.

```python
mm = KotMutableMap({"a": 1, "b": 2, "c": 3})

# Remove by key
value = mm.remove("b")  # Returns 2

# Remove only if value matches
removed = mm.remove_value("c", 3)  # Returns True
not_removed = mm.remove_value("a", 10)  # Returns False
```

#### clear()

Removes all key/value pairs from the map.

```python
mm = KotMutableMap({"a": 1, "b": 2, "c": 3})
mm.clear()
print(mm.is_empty())  # True
```

### Advanced Mutation Operations

#### get_or_put(key, default_value)

Returns the value for the given key. If not found, calls defaultValue and puts its result.

```python
mm = KotMutableMap({"a": 1})
value = mm.get_or_put("b", lambda: 2 * 2)
print(value)  # 4
print(mm.to_dict())  # {'a': 1, 'b': 4}
```

#### compute(key, remapping_function)

Attempts to compute a mapping for the specified key and its current mapped value.

```python
mm = KotMutableMap({"a": 1, "b": 2})

# Update existing value
mm.compute("a", lambda k, v: v * 10 if v else 1)
print(mm.get("a"))  # 10

# Add new value
mm.compute("c", lambda k, v: 3 if v is None else v)
print(mm.get("c"))  # 3
```

#### compute_if_absent(key, mapping_function)

Computes value only if the key is not already associated with a value.

```python
mm = KotMutableMap({"a": 1})
value1 = mm.compute_if_absent("a", lambda k: len(k))  # Returns 1
value2 = mm.compute_if_absent("hello", lambda k: len(k))  # Returns 5
print(mm.to_dict())  # {'a': 1, 'hello': 5}
```

#### compute_if_present(key, remapping_function)

Computes a new mapping only if the value for the key is present.

```python
mm = KotMutableMap({"a": 1, "b": 2})
new_val = mm.compute_if_present("a", lambda k, v: v * 10)  # Returns 10
no_val = mm.compute_if_present("c", lambda k, v: v * 10)  # Returns None
```

#### replace(key, value) / replace_all(transform)

Replace values in the map.

```python
mm = KotMutableMap({"a": 1, "b": 2, "c": 3})

# Replace single value if key exists
old = mm.replace("a", 10)  # Returns 1
none = mm.replace("d", 4)  # Returns None (key didn't exist)

# Replace all values
mm.replace_all(lambda k, v: v * 2)
print(mm.to_dict())  # {'a': 20, 'b': 4, 'c': 6}
```

#### merge(key, value, remapping_function)

Merges a value with an existing value using the remapping function.

```python
mm = KotMutableMap({"a": "Hello"})
mm.merge("a", " World", lambda old, new: old + new)
print(mm.get("a"))  # "Hello World"

mm.merge("b", "Hi", lambda old, new: old + new)
print(mm.get("b"))  # "Hi"
```

#### plus_assign(other) / minus_assign(key)

In-place operations for adding/removing entries.

```python
mm = KotMutableMap({"a": 1, "b": 2})

# Add entries
mm.plus_assign({"c": 3, "d": 4})
mm += ("e", 5)  # Operator shortcut

# Remove entries
mm.minus_assign("a")
mm -= "b"  # Operator shortcut
```

## Performance Considerations

- `KotList` internally uses Python's standard list, so basic operation performance is equivalent to standard lists
- `KotSet` internally uses Python's standard set, providing O(1) average case for add, remove, and contains operations
- `KotMap` internally uses Python's standard dict, providing O(1) average case for get, put, and contains operations
- When using method chaining extensively, be aware that each method creates a new collection, which may impact memory
  usage
- For large datasets, consider generator-based implementations