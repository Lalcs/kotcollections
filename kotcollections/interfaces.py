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
    TypeVar, Generic, Callable, Optional, Iterator, Tuple, Any, Iterable, List, Set, Dict
)

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
R = TypeVar('R')
K = TypeVar('K')
V = TypeVar('V')
K_co = TypeVar('K_co', covariant=True)
V_co = TypeVar('V_co', covariant=True)


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
    # KotSet inherits all methods from KotCollection
    # No additional abstract methods are required
    pass


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
    # KotMutableSet inherits all methods from KotMutableCollection and KotSet
    # No additional abstract methods are required
    pass


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
    def remove(self, key: K) -> Optional[V]:
        """Removes the specified key and its corresponding value from this map.

        Returns:
            The value associated with the key, or null if the key was not present.
        """
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


