"""
Kotlin-style extension function interfaces for Python collections.

These interfaces define the extension functions that Kotlin provides for collections.
In Kotlin, these are defined as extension functions on Iterable, Collection, List, etc.
In Python, we implement them as mixin interfaces.

Extension interfaces:
- KotlinIterableExtensions[T] - filter, map, fold, reduce, etc.
- KotlinListExtensions[T] - List-specific extensions (sorted, binary_search, etc.)
- KotlinMapExtensions[K, V] - Map-specific extensions
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    TypeVar, Generic, Callable, Optional, Iterator, Tuple, Any, Iterable, Union, TYPE_CHECKING
)

if TYPE_CHECKING:
    from kotcollections.kot_list import KotList
    from kotcollections.kot_set import KotSet
    from kotcollections.kot_map import KotMap

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
R = TypeVar('R')
K = TypeVar('K')
V = TypeVar('V')


# =============================================================================
# Iterable Extensions
# =============================================================================

class KotlinIterableExtensions(ABC, Generic[T_co]):
    """Extension functions for Iterable collections.

    Corresponds to Kotlin's extension functions on Iterable<T>.
    These include transformation, filtering, aggregation, and iteration operations.
    """

    # -------------------------------------------------------------------------
    # Transformation operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def map(self, transform: Callable[[T_co], R]) -> 'KotList[R]':
        """Returns a list containing the results of applying the given transform function."""
        ...

    @abstractmethod
    def map_indexed(self, transform: Callable[[int, T_co], R]) -> 'KotList[R]':
        """Returns a list containing the results of applying the given transform function with index."""
        ...

    @abstractmethod
    def map_not_null(self, transform: Callable[[T_co], Optional[R]]) -> 'KotList[R]':
        """Returns a list containing only the non-null results of applying the given transform."""
        ...

    @abstractmethod
    def flat_map(self, transform: Callable[[T_co], Iterable[R]]) -> 'KotList[R]':
        """Returns a single list of all elements yielded from results of transform function."""
        ...

    # -------------------------------------------------------------------------
    # Filtering operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def filter(self, predicate: Callable[[T_co], bool]) -> 'KotList[T_co]':
        """Returns a list containing only elements matching the given predicate."""
        ...

    @abstractmethod
    def filter_indexed(self, predicate: Callable[[int, T_co], bool]) -> 'KotList[T_co]':
        """Returns a list containing only elements matching the given predicate with index."""
        ...

    @abstractmethod
    def filter_not(self, predicate: Callable[[T_co], bool]) -> 'KotList[T_co]':
        """Returns a list containing all elements not matching the given predicate."""
        ...

    @abstractmethod
    def filter_not_null(self) -> 'KotList[T_co]':
        """Returns a list containing all elements that are not null."""
        ...

    @abstractmethod
    def filter_is_instance(self, klass: type) -> 'KotList[Any]':
        """Returns a list containing all elements that are instances of specified class."""
        ...

    # -------------------------------------------------------------------------
    # Aggregation operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def fold(self, initial: R, operation: Callable[[R, T_co], R]) -> R:
        """Accumulates value starting with initial and applying operation from left to right."""
        ...

    @abstractmethod
    def reduce(self, operation: Callable[[T_co, T_co], T_co]) -> T_co:
        """Accumulates value starting with the first element and applying operation from left to right."""
        ...

    @abstractmethod
    def sum_of(self, selector: Callable[[T_co], Union[int, float]]) -> Union[int, float]:
        """Returns the sum of all values produced by selector function."""
        ...

    @abstractmethod
    def count(self, predicate: Optional[Callable[[T_co], bool]] = None) -> int:
        """Returns the number of elements matching the given predicate, or total count if no predicate."""
        ...

    @abstractmethod
    def max_or_null(self) -> Optional[T_co]:
        """Returns the largest element or null if there are no elements."""
        ...

    @abstractmethod
    def min_or_null(self) -> Optional[T_co]:
        """Returns the smallest element or null if there are no elements."""
        ...

    @abstractmethod
    def max_by_or_null(self, selector: Callable[[T_co], Any]) -> Optional[T_co]:
        """Returns the first element yielding the largest value of the given function or null."""
        ...

    @abstractmethod
    def min_by_or_null(self, selector: Callable[[T_co], Any]) -> Optional[T_co]:
        """Returns the first element yielding the smallest value of the given function or null."""
        ...

    # -------------------------------------------------------------------------
    # Testing operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def any(self, predicate: Optional[Callable[[T_co], bool]] = None) -> bool:
        """Returns true if at least one element matches the given predicate."""
        ...

    @abstractmethod
    def all(self, predicate: Callable[[T_co], bool]) -> bool:
        """Returns true if all elements match the given predicate."""
        ...

    @abstractmethod
    def none(self, predicate: Optional[Callable[[T_co], bool]] = None) -> bool:
        """Returns true if no elements match the given predicate."""
        ...

    # -------------------------------------------------------------------------
    # Finding operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def find(self, predicate: Callable[[T_co], bool]) -> Optional[T_co]:
        """Returns the first element matching the given predicate, or null if not found."""
        ...

    @abstractmethod
    def find_last(self, predicate: Callable[[T_co], bool]) -> Optional[T_co]:
        """Returns the last element matching the given predicate, or null if not found."""
        ...

    # -------------------------------------------------------------------------
    # Grouping operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def group_by(self, key_selector: Callable[[T_co], K]) -> 'KotMap[K, KotList[T_co]]':
        """Groups elements by the key returned by the given key_selector function."""
        ...

    @abstractmethod
    def partition(self, predicate: Callable[[T_co], bool]) -> Tuple['KotList[T_co]', 'KotList[T_co]']:
        """Splits the collection into pair of lists (matching, not matching)."""
        ...

    # -------------------------------------------------------------------------
    # Distinct operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def distinct(self) -> 'KotList[T_co]':
        """Returns a list containing only distinct elements."""
        ...

    @abstractmethod
    def distinct_by(self, selector: Callable[[T_co], Any]) -> 'KotList[T_co]':
        """Returns a list containing only elements having distinct keys returned by selector."""
        ...

    # -------------------------------------------------------------------------
    # Iteration operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def for_each(self, action: Callable[[T_co], None]) -> None:
        """Performs the given action on each element."""
        ...

    @abstractmethod
    def for_each_indexed(self, action: Callable[[int, T_co], None]) -> None:
        """Performs the given action on each element with its index."""
        ...

    @abstractmethod
    def on_each(self, action: Callable[[T_co], None]) -> 'KotlinIterableExtensions[T_co]':
        """Performs the given action on each element and returns the collection itself."""
        ...

    # -------------------------------------------------------------------------
    # Joining operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def join_to_string(
        self,
        separator: str = ", ",
        prefix: str = "",
        postfix: str = "",
        limit: int = -1,
        truncated: str = "...",
        transform: Optional[Callable[[T_co], str]] = None
    ) -> str:
        """Creates a string from all the elements separated using separator."""
        ...

    # -------------------------------------------------------------------------
    # Conversion operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def to_list(self) -> list:
        """Returns a Python list containing all elements."""
        ...

    @abstractmethod
    def to_set(self) -> set:
        """Returns a Python set containing all distinct elements."""
        ...

    @abstractmethod
    def to_kot_list(self) -> 'KotList[T_co]':
        """Returns a KotList containing all elements."""
        ...

    @abstractmethod
    def to_kot_set(self) -> 'KotSet[T_co]':
        """Returns a KotSet containing all distinct elements."""
        ...


# =============================================================================
# List Extensions
# =============================================================================

class KotlinListExtensions(KotlinIterableExtensions[T_co]):
    """Extension functions specific to List collections.

    Corresponds to Kotlin's extension functions on List<T>.
    Includes sorting, slicing, and index-based operations.
    """

    # -------------------------------------------------------------------------
    # Sorting operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def sorted(self, key: Optional[Callable[[T_co], Any]] = None, reverse: bool = False) -> 'KotList[T_co]':
        """Returns a list of all elements sorted according to natural sort order."""
        ...

    @abstractmethod
    def sorted_by(self, selector: Callable[[T_co], Any]) -> 'KotList[T_co]':
        """Returns a list of all elements sorted according to the specified selector."""
        ...

    @abstractmethod
    def sorted_descending(self) -> 'KotList[T_co]':
        """Returns a list of all elements sorted descending according to natural sort order."""
        ...

    @abstractmethod
    def sorted_by_descending(self, selector: Callable[[T_co], Any]) -> 'KotList[T_co]':
        """Returns a list of all elements sorted descending according to the specified selector."""
        ...

    @abstractmethod
    def reversed(self) -> 'KotList[T_co]':
        """Returns a list with elements in reversed order."""
        ...

    @abstractmethod
    def shuffled(self) -> 'KotList[T_co]':
        """Returns a list with elements shuffled."""
        ...

    # -------------------------------------------------------------------------
    # Slicing operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def take(self, n: int) -> 'KotList[T_co]':
        """Returns a list containing first n elements."""
        ...

    @abstractmethod
    def take_last(self, n: int) -> 'KotList[T_co]':
        """Returns a list containing last n elements."""
        ...

    @abstractmethod
    def take_while(self, predicate: Callable[[T_co], bool]) -> 'KotList[T_co]':
        """Returns a list containing first elements satisfying the given predicate."""
        ...

    @abstractmethod
    def drop(self, n: int) -> 'KotList[T_co]':
        """Returns a list containing all elements except first n elements."""
        ...

    @abstractmethod
    def drop_last(self, n: int) -> 'KotList[T_co]':
        """Returns a list containing all elements except last n elements."""
        ...

    @abstractmethod
    def drop_while(self, predicate: Callable[[T_co], bool]) -> 'KotList[T_co]':
        """Returns a list containing all elements except first elements satisfying the given predicate."""
        ...

    # -------------------------------------------------------------------------
    # Chunking operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def chunked(self, size: int) -> 'KotList[KotList[T_co]]':
        """Splits this collection into a list of lists each not exceeding the given size."""
        ...

    @abstractmethod
    def windowed(
        self,
        size: int,
        step: int = 1,
        partial_windows: bool = False
    ) -> 'KotList[KotList[T_co]]':
        """Returns a list of snapshots of the window of the given size sliding along this collection."""
        ...

    # -------------------------------------------------------------------------
    # Zip operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def zip(self, other: Iterable[R]) -> 'KotList[Tuple[T_co, R]]':
        """Returns a list of pairs built from elements of both collections."""
        ...

    @abstractmethod
    def zip_with_next(self) -> 'KotList[Tuple[T_co, T_co]]':
        """Returns a list of pairs of each two adjacent elements."""
        ...

    # -------------------------------------------------------------------------
    # Set operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def plus(self, elements: Union[T_co, Iterable[T_co]]) -> 'KotList[T_co]':
        """Returns a list containing all elements of the original collection and then all given elements."""
        ...

    @abstractmethod
    def minus(self, elements: Union[T_co, Iterable[T_co]]) -> 'KotList[T_co]':
        """Returns a list containing all elements of the original collection except the given elements."""
        ...

    @abstractmethod
    def union(self, other: Iterable[T_co]) -> 'KotSet[T_co]':
        """Returns a set containing all distinct elements from both collections."""
        ...

    @abstractmethod
    def intersect(self, other: Iterable[T_co]) -> 'KotSet[T_co]':
        """Returns a set containing all elements that are contained by both collections."""
        ...

    @abstractmethod
    def subtract(self, other: Iterable[T_co]) -> 'KotSet[T_co]':
        """Returns a set containing all elements of this collection that are not in the other collection."""
        ...


# =============================================================================
# Map Extensions
# =============================================================================

class KotlinMapExtensions(ABC, Generic[K, V]):
    """Extension functions specific to Map collections.

    Corresponds to Kotlin's extension functions on Map<K, V>.
    """

    # -------------------------------------------------------------------------
    # Transformation operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def map(self, transform: Callable[[K, V], R]) -> 'KotList[R]':
        """Returns a list containing results of applying the given transform to each entry."""
        ...

    @abstractmethod
    def map_keys(self, transform: Callable[[K, V], R]) -> 'KotMap[R, V]':
        """Returns a new map with entries having keys obtained by applying transform."""
        ...

    @abstractmethod
    def map_values(self, transform: Callable[[K, V], R]) -> 'KotMap[K, R]':
        """Returns a new map with entries having values obtained by applying transform."""
        ...

    @abstractmethod
    def flat_map(self, transform: Callable[[K, V], Iterable[R]]) -> 'KotList[R]':
        """Returns a single list of all elements yielded from results of transform function."""
        ...

    # -------------------------------------------------------------------------
    # Filtering operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def filter(self, predicate: Callable[[K, V], bool]) -> 'KotMap[K, V]':
        """Returns a map containing all entries matching the given predicate."""
        ...

    @abstractmethod
    def filter_keys(self, predicate: Callable[[K], bool]) -> 'KotMap[K, V]':
        """Returns a map containing all entries with keys matching the given predicate."""
        ...

    @abstractmethod
    def filter_values(self, predicate: Callable[[V], bool]) -> 'KotMap[K, V]':
        """Returns a map containing all entries with values matching the given predicate."""
        ...

    # -------------------------------------------------------------------------
    # Testing operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def any(self, predicate: Callable[[K, V], bool]) -> bool:
        """Returns true if at least one entry matches the given predicate."""
        ...

    @abstractmethod
    def all(self, predicate: Callable[[K, V], bool]) -> bool:
        """Returns true if all entries match the given predicate."""
        ...

    @abstractmethod
    def none(self, predicate: Callable[[K, V], bool]) -> bool:
        """Returns true if no entries match the given predicate."""
        ...

    # -------------------------------------------------------------------------
    # Iteration operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def for_each(self, action: Callable[[K, V], None]) -> None:
        """Performs the given action on each entry."""
        ...

    @abstractmethod
    def on_each(self, action: Callable[[K, V], None]) -> 'KotlinMapExtensions[K, V]':
        """Performs the given action on each entry and returns the map itself."""
        ...

    # -------------------------------------------------------------------------
    # Operator operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def plus(self, other: Union['KotMap[K, V]', dict, Tuple[K, V]]) -> 'KotMap[K, V]':
        """Returns a map containing all entries of this map and the given map/pair."""
        ...

    @abstractmethod
    def minus(self, key: Union[K, Iterable[K]]) -> 'KotMap[K, V]':
        """Returns a map containing all entries except those with the given keys."""
        ...
