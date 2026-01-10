"""
Kotlin-style collection interfaces for Python.

This module defines abstract interfaces that mirror Kotlin's collection hierarchy.

Immutable (read-only):
- KotlinIterable[T] - Base interface for iteration
- KotlinCollection[T] - Sized, iterable collection with contains
- KotlinList[T] - Ordered collection with index-based access
- KotlinSet[T] - Collection with unique elements
- KotlinMap[K, V] - Key-value pairs

Mutable:
- KotlinMutableIterable[T]
- KotlinMutableCollection[T] - Collection with add/remove operations
- KotlinMutableList[T] - List with mutation operations
- KotlinMutableSet[T] - Set with mutation operations
- KotlinMutableMap[K, V] - Map with mutation operations
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    TypeVar, Generic, Callable, Optional, Iterator, Tuple, Any, Iterable, List, Set, Dict, Type
)

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
R = TypeVar('R')
K = TypeVar('K')
V = TypeVar('V')
K_co = TypeVar('K_co', covariant=True)
V_co = TypeVar('V_co', covariant=True)


# =============================================================================
# Factory Mixin Interfaces
# =============================================================================

class KotlinCollectionFactory(ABC, Generic[T_co]):
    """Factory method mixin for creating typed collections.

    Provides the of_type() class method for creating collections with explicit type checking.
    """

    @classmethod
    @abstractmethod
    def of_type(cls, element_type: Type[T_co], elements: Optional[Iterable[T_co]] = None) -> 'KotlinCollectionFactory[T_co]':
        """Create a collection with a specific element type.

        Args:
            element_type: The type of elements this collection will contain.
            elements: Optional initial elements.

        Returns:
            A new collection instance with the specified element type.
        """
        ...


class KotlinMapFactory(ABC, Generic[K_co, V_co]):
    """Factory method mixin for creating typed maps.

    Provides the of_type() class method for creating maps with explicit type checking.
    """

    @classmethod
    @abstractmethod
    def of_type(cls, key_type: Type[K_co], value_type: Type[V_co], elements: Optional[Dict[K_co, V_co]] = None) -> 'KotlinMapFactory[K_co, V_co]':
        """Create a map with specific key and value types.

        Args:
            key_type: The type of keys this map will contain.
            value_type: The type of values this map will contain.
            elements: Optional initial elements.

        Returns:
            A new map instance with the specified key and value types.
        """
        ...


# =============================================================================
# Immutable (Read-only) Interfaces
# =============================================================================

class KotlinIterable(ABC, Generic[T_co]):
    """Base interface for all iterable collections.

    Corresponds to Kotlin's Iterable<T> interface.
    """

    @abstractmethod
    def __iter__(self) -> Iterator[T_co]:
        """Returns an iterator over the elements of this collection."""
        ...


class KotlinCollection(KotlinIterable[T_co]):
    """A generic collection of elements with size and contains operations.

    Corresponds to Kotlin's Collection<T> interface.
    """

    @property
    @abstractmethod
    def size(self) -> int:
        """Returns the size of the collection."""
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns true if the collection is empty."""
        ...

    @abstractmethod
    def is_not_empty(self) -> bool:
        """Returns true if the collection is not empty."""
        ...

    @abstractmethod
    def contains(self, element: Any) -> bool:
        """Returns true if the collection contains the specified element."""
        ...

    @abstractmethod
    def contains_all(self, elements: Iterable[Any]) -> bool:
        """Returns true if the collection contains all of the specified elements."""
        ...

    def __len__(self) -> int:
        """Return the size of the collection."""
        return self.size

    def __contains__(self, item: Any) -> bool:
        """Check if item is in the collection."""
        return self.contains(item)


class KotlinList(KotlinCollection[T_co]):
    """An ordered collection with index-based access.

    Corresponds to Kotlin's List<T> interface.
    """

    @abstractmethod
    def get(self, index: int) -> T_co:
        """Returns the element at the specified index."""
        ...

    @abstractmethod
    def get_or_null(self, index: int) -> Optional[T_co]:
        """Returns the element at the specified index, or null if the index is out of bounds."""
        ...


    @abstractmethod
    def index_of(self, element: Any) -> int:
        """Returns the index of the first occurrence of the specified element, or -1 if not found."""
        ...

    @abstractmethod
    def last_index_of(self, element: Any) -> int:
        """Returns the index of the last occurrence of the specified element, or -1 if not found."""
        ...

    @abstractmethod
    def first(self) -> T_co:
        """Returns the first element."""
        ...

    @abstractmethod
    def first_or_null(self) -> Optional[T_co]:
        """Returns the first element, or null if the collection is empty."""
        ...


    @abstractmethod
    def last(self) -> T_co:
        """Returns the last element."""
        ...

    @abstractmethod
    def last_or_null(self) -> Optional[T_co]:
        """Returns the last element, or null if the collection is empty."""
        ...


    @abstractmethod
    def sub_list(self, from_index: int, to_index: int) -> 'KotlinList[T_co]':
        """Returns a view of the portion of this list between the specified fromIndex (inclusive) and toIndex (exclusive)."""
        ...

    @property
    @abstractmethod
    def indices(self) -> range:
        """Returns the range of valid indices for this list."""
        ...

    @property
    @abstractmethod
    def last_index(self) -> int:
        """Returns the index of the last element, or -1 if the list is empty."""
        ...

    def __getitem__(self, index: int) -> T_co:
        """Get element by index using [] operator."""
        return self.get(index)


class KotlinSet(KotlinCollection[T_co]):
    """A collection with unique elements.

    Corresponds to Kotlin's Set<T> interface.
    """

    @abstractmethod
    def first(self) -> T_co:
        """Returns the first element."""
        ...

    @abstractmethod
    def first_or_null(self) -> Optional[T_co]:
        """Returns the first element, or null if the set is empty."""
        ...

    @abstractmethod
    def last(self) -> T_co:
        """Returns the last element."""
        ...

    @abstractmethod
    def last_or_null(self) -> Optional[T_co]:
        """Returns the last element, or null if the set is empty."""
        ...

    @abstractmethod
    def single(self) -> T_co:
        """Returns the single element, or throws if the set is empty or has more than one element."""
        ...

    @abstractmethod
    def single_or_null(self) -> Optional[T_co]:
        """Returns the single element, or null if the set is empty or has more than one element."""
        ...


class KotlinMap(ABC, Generic[K_co, V_co]):
    """A collection of key-value pairs.

    Corresponds to Kotlin's Map<K, V> interface.
    """

    @property
    @abstractmethod
    def size(self) -> int:
        """Returns the number of key/value pairs in the map."""
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns true if the map is empty."""
        ...

    @abstractmethod
    def is_not_empty(self) -> bool:
        """Returns true if the map is not empty."""
        ...

    @abstractmethod
    def contains_key(self, key: Any) -> bool:
        """Returns true if the map contains the specified key."""
        ...

    @abstractmethod
    def contains_value(self, value: Any) -> bool:
        """Returns true if the map maps one or more keys to the specified value."""
        ...

    @abstractmethod
    def get(self, key: Any) -> Optional[V_co]:
        """Returns the value corresponding to the given key, or null if such a key is not present."""
        ...

    @abstractmethod
    def get_or_default(self, key: Any, default_value: V_co) -> V_co:
        """Returns the value corresponding to the given key, or default_value if such a key is not present."""
        ...

    @abstractmethod
    def get_or_else(self, key: Any, default_value: Callable[[], V_co]) -> V_co:
        """Returns the value for the given key. If the key is not found, calls the defaultValue function."""
        ...

    @abstractmethod
    def get_value(self, key: Any) -> V_co:
        """Returns the value for the given key or throws an exception if the key is missing."""
        ...

    @property
    @abstractmethod
    def keys(self) -> 'KotlinSet[K_co]':
        """Returns a read-only Set of all keys in this map."""
        ...

    @property
    @abstractmethod
    def values(self) -> 'KotlinCollection[V_co]':
        """Returns a read-only Collection of all values in this map."""
        ...

    @property
    @abstractmethod
    def entries(self) -> 'KotlinSet[Tuple[K_co, V_co]]':
        """Returns a read-only Set of all key/value pairs in this map."""
        ...

    def __len__(self) -> int:
        """Return the number of entries in the map."""
        return self.size

    def __contains__(self, key: Any) -> bool:
        """Check if a key is in the map."""
        return self.contains_key(key)

    def __getitem__(self, key: Any) -> V_co:
        """Get value by key using [] operator."""
        return self.get_value(key)

    @abstractmethod
    def __iter__(self) -> Iterator[K_co]:
        """Iterate over keys."""
        ...


# =============================================================================
# Mutable Interfaces
# =============================================================================

class KotlinMutableIterable(KotlinIterable[T]):
    """A mutable iterable that can be modified during iteration.

    Corresponds to Kotlin's MutableIterable<T> interface.
    """
    pass


class KotlinMutableCollection(KotlinCollection[T], KotlinMutableIterable[T]):
    """A mutable collection that supports adding and removing elements.

    Corresponds to Kotlin's MutableCollection<T> interface.
    """

    @abstractmethod
    def add(self, element: T) -> bool:
        """Adds the specified element to the collection.

        Returns:
            true if the element has been added, false if the collection does not support duplicates
            and the element is already contained in the collection.
        """
        ...

    @abstractmethod
    def add_all(self, elements: Iterable[T]) -> bool:
        """Adds all of the elements in the specified collection to this collection.

        Returns:
            true if any of the specified elements was added to the collection.
        """
        ...

    @abstractmethod
    def remove(self, element: T) -> bool:
        """Removes a single instance of the specified element from this collection.

        Returns:
            true if the element has been successfully removed.
        """
        ...

    @abstractmethod
    def remove_all(self, elements: Iterable[T]) -> bool:
        """Removes all of this collection's elements that are also contained in the specified collection.

        Returns:
            true if any of the specified elements was removed from the collection.
        """
        ...

    @abstractmethod
    def retain_all(self, elements: Iterable[T]) -> bool:
        """Retains only the elements in this collection that are contained in the specified collection.

        Returns:
            true if any element was removed from the collection.
        """
        ...

    @abstractmethod
    def clear(self) -> None:
        """Removes all elements from this collection."""
        ...


class KotlinMutableList(KotlinList[T], KotlinMutableCollection[T]):
    """A mutable ordered collection with index-based access and modification.

    Corresponds to Kotlin's MutableList<T> interface.
    """

    @abstractmethod
    def add_at(self, index: int, element: T) -> None:
        """Inserts an element at the specified index."""
        ...

    @abstractmethod
    def add_all_at(self, index: int, elements: Iterable[T]) -> bool:
        """Inserts all of the elements in the specified collection into this list at the specified position.

        Returns:
            true if any elements were added.
        """
        ...

    @abstractmethod
    def set(self, index: int, element: T) -> T:
        """Replaces the element at the specified position with the specified element.

        Returns:
            The element previously at the specified position.
        """
        ...

    @abstractmethod
    def remove_at(self, index: int) -> T:
        """Removes an element at the specified index from the list.

        Returns:
            The element that has been removed.
        """
        ...

    @abstractmethod
    def remove_first(self) -> T:
        """Removes the first element from this list and returns it.

        Raises:
            NoSuchElementException: if the list is empty.
        """
        ...

    @abstractmethod
    def remove_first_or_null(self) -> Optional[T]:
        """Removes the first element from this list and returns it, or returns null if the list is empty."""
        ...

    @abstractmethod
    def remove_last(self) -> T:
        """Removes the last element from this list and returns it.

        Raises:
            NoSuchElementException: if the list is empty.
        """
        ...

    @abstractmethod
    def remove_last_or_null(self) -> Optional[T]:
        """Removes the last element from this list and returns it, or returns null if the list is empty."""
        ...

    @abstractmethod
    def remove_if(self, predicate: Callable[[T], bool]) -> bool:
        """Removes all elements from this list that match the given predicate.

        Returns:
            true if any elements were removed.
        """
        ...

    @abstractmethod
    def replace_all(self, operator: Callable[[T], T]) -> None:
        """Replaces each element of this list with the result of applying the operator to that element."""
        ...

    @abstractmethod
    def reverse(self) -> None:
        """Reverses the elements in this list in place."""
        ...

    @abstractmethod
    def shuffle(self) -> None:
        """Randomly shuffles elements in this list in place."""
        ...

    @abstractmethod
    def sort(self) -> None:
        """Sorts elements in this list in place according to their natural sort order."""
        ...

    @abstractmethod
    def sort_by(self, selector: Callable[[T], Any]) -> None:
        """Sorts elements in this list in place according to the value returned by the selector function."""
        ...

    @abstractmethod
    def sort_by_descending(self, selector: Callable[[T], Any]) -> None:
        """Sorts elements in this list in place in descending order according to the value returned by the selector."""
        ...

    @abstractmethod
    def sort_descending(self) -> None:
        """Sorts elements in this list in place in descending order according to their natural sort order."""
        ...

    @abstractmethod
    def sort_with(self, comparator: Callable[[T, T], int]) -> None:
        """Sorts elements in this list in place according to the order specified by the comparator."""
        ...

    @abstractmethod
    def fill(self, value: T) -> None:
        """Fills this list with the provided value."""
        ...

    def __setitem__(self, index: int, value: T) -> None:
        """Set element by index using [] operator."""
        self.set(index, value)

    def __delitem__(self, index: int) -> None:
        """Delete element by index using del operator."""
        self.remove_at(index)


class KotlinMutableSet(KotlinSet[T], KotlinMutableCollection[T]):
    """A mutable collection with unique elements that supports adding and removing.

    Corresponds to Kotlin's MutableSet<T> interface.
    """

    @abstractmethod
    def remove_if(self, predicate: Callable[[T], bool]) -> bool:
        """Removes all elements from this set that match the given predicate.

        Returns:
            true if any elements were removed.
        """
        ...

    @abstractmethod
    def retain_if(self, predicate: Callable[[T], bool]) -> bool:
        """Retains only the elements in this set that match the given predicate.

        Returns:
            true if any elements were removed.
        """
        ...

    @abstractmethod
    def union_update(self, other: Iterable[T]) -> None:
        """Adds all elements from the other collection to this set."""
        ...

    @abstractmethod
    def intersect_update(self, other: Iterable[T]) -> None:
        """Retains only elements that are present in both this set and the other collection."""
        ...

    @abstractmethod
    def subtract_update(self, other: Iterable[T]) -> None:
        """Removes all elements from this set that are contained in the other collection."""
        ...


class KotlinMutableMap(KotlinMap[K, V]):
    """A mutable collection of key-value pairs that supports adding and removing entries.

    Corresponds to Kotlin's MutableMap<K, V> interface.
    """

    @abstractmethod
    def put(self, key: K, value: V) -> Optional[V]:
        """Associates the specified value with the specified key in the map.

        Returns:
            The previous value associated with the key, or null if the key was not present.
        """
        ...

    @abstractmethod
    def put_all(self, from_map: Dict[K, V]) -> None:
        """Updates this map with key/value pairs from the specified map."""
        ...

    @abstractmethod
    def put_if_absent(self, key: K, value: V) -> Optional[V]:
        """Associates the specified value with the specified key only if the key is not present.

        Returns:
            The current value associated with the key, or null if inserted.
        """
        ...

    @abstractmethod
    def remove(self, key: K) -> Optional[V]:
        """Removes the specified key and its corresponding value from this map.

        Returns:
            The value associated with the key, or null if the key was not present.
        """
        ...

    @abstractmethod
    def remove_value(self, key: K, value: V) -> bool:
        """Removes the entry for the specified key only if it is mapped to the specified value.

        Returns:
            true if the entry was removed.
        """
        ...

    @abstractmethod
    def get_or_put(self, key: K, default_value: Callable[[], V]) -> V:
        """Returns the value for the given key. If the key is not present, calls defaultValue,
        puts the result into the map, and returns it.
        """
        ...

    @abstractmethod
    def compute(self, key: K, remapping_function: Callable[[K, Optional[V]], Optional[V]]) -> Optional[V]:
        """Attempts to compute a mapping for the specified key and its current mapped value.

        Returns:
            The new value associated with the key, or null if none.
        """
        ...

    @abstractmethod
    def compute_if_absent(self, key: K, mapping_function: Callable[[K], V]) -> V:
        """Computes a value for the specified key only if the key is not present.

        Returns:
            The current (existing or computed) value associated with the key.
        """
        ...

    @abstractmethod
    def compute_if_present(self, key: K, remapping_function: Callable[[K, V], Optional[V]]) -> Optional[V]:
        """Computes a new value for the specified key only if a value is already present.

        Returns:
            The new value associated with the key, or null if removed.
        """
        ...

    @abstractmethod
    def merge(self, key: K, value: V, remapping_function: Callable[[V, V], V]) -> V:
        """Merges the specified value with the existing value using the given function.

        Returns:
            The new value associated with the key.
        """
        ...

    @abstractmethod
    def replace(self, key: K, value: V) -> Optional[V]:
        """Replaces the entry for the specified key only if it is currently mapped.

        Returns:
            The previous value associated with the key, or null if not present.
        """
        ...

    @abstractmethod
    def replace_all(self, function: Callable[[K, V], V]) -> None:
        """Replaces each entry's value with the result of invoking the given function."""
        ...

    @abstractmethod
    def pop(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Removes and returns the value for the specified key, or default if not present."""
        ...

    @abstractmethod
    def popitem(self) -> Tuple[K, V]:
        """Removes and returns an arbitrary (key, value) pair from the map.

        Raises:
            KeyError: if the map is empty.
        """
        ...

    @abstractmethod
    def update(self, other: Dict[K, V]) -> None:
        """Updates this map with key/value pairs from the specified dictionary."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Removes all key/value pairs from the map."""
        ...

    def __setitem__(self, key: K, value: V) -> None:
        """Set value by key using [] operator."""
        self.put(key, value)

    def __delitem__(self, key: K) -> None:
        """Delete entry by key using del operator."""
        self.remove(key)


# =============================================================================
# Pythonic Alias Mixin Interfaces
# =============================================================================

class PythonicListAliases(ABC, Generic[T_co]):
    """Pythonic aliases for KotlinList methods (_or_null → _or_none).

    This mixin provides Python-style method names using 'None' instead of 'null'.
    Implementations should delegate to the corresponding _or_null methods.
    """

    @abstractmethod
    def get_or_none(self, index: int) -> Optional[T_co]:
        """Alias for get_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def first_or_none(self) -> Optional[T_co]:
        """Alias for first_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def last_or_none(self) -> Optional[T_co]:
        """Alias for last_or_null() - more Pythonic naming."""
        ...


