# KotList - Kotlin List API for Python

KotList is a Python library that fully reproduces Kotlin's List interface. It brings Kotlin's rich collection operations
to Python developers.

## Installation

```bash
pip install kotlist
```

## Features

- Complete implementation of all Kotlin List methods using Python's snake_case naming convention
- Provides both read-only `KotList` and mutable `KotMutableList`
- Full type safety with type hints
- Runtime type checking to ensure single element type (similar to Kotlin's generic type system)
- 100% test coverage

## Type Safety

KotList implements runtime type checking similar to Kotlin's type system. Once a list is created with elements of a
specific type, it can only contain elements of that same type.

### How It Works

- The first element added to a KotList determines its element type
- All subsequent elements must be of the same type
- KotList instances can be nested (similar to `List<List<T>>` in Kotlin)
- Type checking occurs on initialization and all modification operations

### Examples

```python
# Valid: All elements are the same type
lst = KotList([1, 2, 3])  # KotList[int]
lst2 = KotList(['a', 'b', 'c'])  # KotList[str]

# Invalid: Mixed types will raise TypeError
try:
    lst = KotList([1, 'a', 2])  # TypeError!
except TypeError as e:
    print(e)  # Cannot add element of type 'str' to KotList[int]

# Valid: Nested KotLists
nested = KotList(
    [
        KotList([1, 2]),
        KotList([3, 4])
    ]
)  # KotList[KotList]

# Mutable lists also enforce type safety
mutable = KotMutableList([1, 2, 3])
mutable.add(4)  # OK: same type

try:
    mutable.add('string')  # TypeError!
except TypeError as e:
    print(e)  # Cannot add element of type 'str' to KotList[int]

# Empty lists determine type on first element
empty = KotMutableList()
empty.add('first')  # Now it's KotList[str]
empty.add('second')  # OK
# empty.add(123)  # Would raise TypeError
```

### Comparison with Kotlin

This type safety implementation provides similar guarantees to Kotlin's generic type system:

| Kotlin            | KotList (Python)                              |
|-------------------|-----------------------------------------------|
| `List<Int>`       | `KotList([1, 2, 3])`                          |
| `List<String>`    | `KotList(['a', 'b', 'c'])`                    |
| `List<List<Int>>` | `KotList([KotList([1, 2]), KotList([3, 4])])` |

The main difference is that Kotlin performs compile-time type checking, while KotList performs runtime type checking.

## Basic Usage

```python
from kotlist import KotList, KotMutableList

# Create a read-only list
lst = KotList([1, 2, 3, 4, 5])

# Create a mutable list
mutable_lst = KotMutableList([1, 2, 3, 4, 5])
```

## Kotlin to Python Naming Convention

| Kotlin            | Python              |
|-------------------|---------------------|
| `getOrNull()`     | `get_or_null()`     |
| `firstOrNull()`   | `first_or_null()`   |
| `mapIndexed()`    | `map_indexed()`     |
| `filterNotNull()` | `filter_not_null()` |
| `associateBy()`   | `associate_by()`    |
| `joinToString()`  | `join_to_string()`  |

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

#### get_or_null(index)

Gets the element at the specified index (returns None if out of range).

```python
lst = KotList([10, 20, 30])
print(lst.get_or_null(1))  # 20
print(lst.get_or_null(10))  # None
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

#### first_or_null() / last_or_null()

Gets the first/last element (returns None if empty).

```python
lst = KotList([10, 20, 30])
print(lst.first_or_null())  # 10

empty = KotList()
print(empty.first_or_null())  # None
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

#### map_not_null(transform)

Creates a new list containing only non-None transformation results.

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

#### filter_not_null()

Creates a new list containing only non-None elements.

```python
lst = KotList([1, None, 2, None, 3])
non_nulls = lst.filter_not_null()
print(non_nulls.to_list())  # [1, 2, 3]
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

#### max_or_null() / min_or_null()

Returns the maximum/minimum value (None if empty).

```python
lst = KotList([3, 1, 4, 1, 5])
print(lst.max_or_null())  # 5
print(lst.min_or_null())  # 1
```

#### max_by_or_null(selector) / min_by_or_null(selector)

Returns the element with the maximum/minimum selector result.

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

## Performance Considerations

- `KotList` internally uses Python's standard list, so basic operation performance is equivalent to standard lists
- When using method chaining extensively, be aware that each method creates a new list, which may impact memory usage
- For large datasets, consider generator-based implementations

## License

MIT License