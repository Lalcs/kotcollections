# kotcollections - Kotlin Collections API for Python

kotcollections is a Python library that fully reproduces Kotlin's Collections interfaces. It brings Kotlin's rich collection operations to Python developers with both List and Set implementations.

## Installation

```bash
pip install kotcollections
```

## Features

- Complete implementation of Kotlin's List and Set interfaces using Python's snake_case naming convention
- Pythonic `_none` aliases for all `_null` methods (e.g., both `first_or_null()` and `first_or_none()` are available)
- Provides read-only and mutable variants:
  - `KotList` and `KotMutableList` for list operations
  - `KotSet` and `KotMutableSet` for set operations
- Full type safety with type hints
- Runtime type checking to ensure single element type (similar to Kotlin's generic type system)
- 100% test coverage

## Type Safety

KotList and KotSet implement runtime type checking similar to Kotlin's type system. Once a collection is created with elements of a specific type, it can only contain elements of that same type.

### How It Works

- The first element added to a collection determines its element type
- All subsequent elements must be of the same type
- Collections can be nested (similar to `List<List<T>>` or `Set<Set<T>>` in Kotlin)
- Type checking occurs on initialization and all modification operations

### Examples

```python
# Valid: All elements are the same type
lst = KotList([1, 2, 3])  # KotList[int]
s = KotSet(['a', 'b', 'c'])  # KotSet[str]

# Invalid: Mixed types will raise TypeError
try:
    lst = KotList([1, 'a', 2])  # TypeError!
except TypeError as e:
    print(e)  # Cannot add element of type 'str' to KotList[int]

# Valid: Nested collections
nested_lists = KotList([
    KotList([1, 2]),
    KotList([3, 4])
])  # KotList[KotList]

nested_sets = KotSet([
    KotSet([1, 2]),
    KotSet([3, 4])
])  # KotSet[KotSet]

# Mutable collections also enforce type safety
mutable_list = KotMutableList([1, 2, 3])
mutable_list.add(4)  # OK: same type

mutable_set = KotMutableSet(['a', 'b', 'c'])
mutable_set.add('d')  # OK: same type

try:
    mutable_list.add('string')  # TypeError!
except TypeError as e:
    print(e)  # Cannot add element of type 'str' to KotList[int]

# Empty collections determine type on first element
empty_list = KotMutableList()
empty_list.add('first')  # Now it's KotList[str]

empty_set = KotMutableSet()
empty_set.add(42)  # Now it's KotSet[int]
```

### Comparison with Kotlin

This type safety implementation provides similar guarantees to Kotlin's generic type system:

| Kotlin            | KotList (Python)                              |
|-------------------|-----------------------------------------------|
| `List<Int>`       | `KotList([1, 2, 3])`                          |
| `List<String>`    | `KotList(['a', 'b', 'c'])`                    |
| `List<List<Int>>` | `KotList([KotList([1, 2]), KotList([3, 4])])` |

The main difference is that Kotlin performs compile-time type checking, while KotList performs runtime type checking.

## Pythonic Aliases

To provide a more Pythonic API, all methods ending with `_null` have corresponding `_none` aliases:

```python
# All these _null methods have _none aliases
lst = KotList([1, 2, None, 3, None])

# Access methods
print(lst.get_or_null(10))        # None
print(lst.get_or_none(10))        # None (same result)
print(lst.first_or_none())        # 1
print(lst.last_or_none())         # None

# Transformation methods  
result = lst.map_not_none(lambda x: x * 2 if x else None)  # [2, 4, 6]

# Filtering
non_empty = lst.filter_not_none()  # KotList([1, 2, 3])

# Aggregation
print(lst.max_or_none())          # 3
print(lst.min_or_none())          # 1
```

Both naming conventions are fully supported and can be used interchangeably based on your preference.

## Quick Start

```python
from kotcollections import KotList, KotMutableList, KotSet, KotMutableSet

# Lists - ordered, allows duplicates
numbers = KotList([1, 2, 3, 2, 1])
print(numbers.distinct().to_list())  # [1, 2, 3]

# Sets - unordered, no duplicates
unique_numbers = KotSet([1, 2, 3, 2, 1])
print(unique_numbers.to_list())  # [1, 2, 3] (order not guaranteed)

# Functional operations work on both
doubled_list = numbers.map(lambda x: x * 2)
doubled_set = unique_numbers.map(lambda x: x * 2)

# Mutable variants allow modifications
mutable_list = KotMutableList([1, 2, 3])
mutable_list.add(4)

mutable_set = KotMutableSet([1, 2, 3])
mutable_set.add(4)
```

## Basic Usage

```python
from kotcollections import KotList, KotMutableList

# Create a read-only list
lst = KotList([1, 2, 3, 4, 5])

# Create a mutable list
mutable_lst = KotMutableList([1, 2, 3, 4, 5])
```

## Kotlin to Python Naming Convention

All Kotlin methods are available with Python's snake_case naming convention. Additionally, all methods ending with `_null` have Pythonic `_none` aliases:

| Kotlin            | Python (Primary)    | Python (Alias)      |
|-------------------|---------------------|---------------------|
| `getOrNull()`     | `get_or_null()`     | `get_or_none()`     |
| `firstOrNull()`   | `first_or_null()`   | `first_or_none()`   |
| `mapIndexed()`    | `map_indexed()`     | -                   |
| `filterNotNull()` | `filter_not_null()` | `filter_not_none()` |
| `associateBy()`   | `associate_by()`    | -                   |
| `joinToString()`  | `join_to_string()`  | -                   |

Note: Both naming styles (`_null` and `_none`) can be used interchangeably based on your preference.

## Methods and Examples

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

Gets the element at the specified index (returns None if out of range). Both `get_or_null()` and `get_or_none()` can be used.

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

Creates a new list containing only non-None transformation results. Both `map_not_null()` and `map_not_none()` can be used.

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

Creates a dictionary with elements as keys.

```python
lst = KotList(['a', 'bb', 'ccc'])
length_map = lst.associate_with(lambda x: len(x))
print(length_map)  # {'a': 1, 'bb': 2, 'ccc': 3}
```

#### associate_by(key_selector)

Creates a dictionary with keys generated from elements.

```python
lst = KotList(['a', 'bb', 'ccc'])
by_length = lst.associate_by(lambda x: len(x))
print(by_length)  # {1: 'a', 2: 'bb', 3: 'ccc'}
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

Groups elements by key.

```python
lst = KotList([1, 2, 3, 4, 5, 6])
by_parity = lst.group_by(lambda x: x % 2)
print(by_parity[0].to_list())  # [2, 4, 6]
print(by_parity[1].to_list())  # [1, 3, 5]
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

Converts to Python set.

```python
lst = KotList([1, 2, 2, 3, 3])
unique_set = lst.to_set()
print(unique_set)  # {1, 2, 3}
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

## KotSet

KotSet is a Python implementation of Kotlin's Set interface, providing a read-only set with rich functional operations.

### Basic Usage

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
grouped = s.group_by(lambda x: x % 2)  # {0: KotSet([2, 4]), 1: KotSet([1, 3, 5])}
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

## KotMutableSet

KotMutableSet extends KotSet with mutation methods, providing a mutable set implementation.

### Basic Usage

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
immutable_set = mutable_set.to_kot_set()  # Returns KotSet

# Convert to Python types
python_set = mutable_set.to_set()  # Returns set
python_list = mutable_set.to_list()  # Returns list
sorted_list = mutable_set.to_sorted_list()  # Returns sorted list
```

## Performance Considerations

- `KotList` internally uses Python's standard list, so basic operation performance is equivalent to standard lists
- `KotSet` internally uses Python's standard set, providing O(1) average case for add, remove, and contains operations
- When using method chaining extensively, be aware that each method creates a new collection, which may impact memory usage
- For large datasets, consider generator-based implementations

## License

MIT License