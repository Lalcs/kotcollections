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

    @abstractmethod
    def average(self) -> float:
        """Returns an average value of elements in the collection."""
        ...

    @abstractmethod
    def reduce_or_null(self, operation: Callable[[T_co, T_co], T_co]) -> Optional[T_co]:
        """Accumulates value or returns null if the collection is empty."""
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

    @abstractmethod
    def first(self) -> T_co:
        """Returns the first element."""
        ...

    @abstractmethod
    def first_or_null(self) -> Optional[T_co]:
        """Returns the first element, or null if the collection is empty."""
        ...

    @abstractmethod
    def first_predicate(self, predicate: Callable[[T_co], bool]) -> T_co:
        """Returns the first element matching the given predicate. Throws if not found."""
        ...

    @abstractmethod
    def first_or_null_predicate(self, predicate: Callable[[T_co], bool]) -> Optional[T_co]:
        """Returns the first element matching the given predicate, or null if not found."""
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
    def single(self) -> T_co:
        """Returns the single element, or throws if the collection is empty or has more than one element."""
        ...

    @abstractmethod
    def single_or_null(self) -> Optional[T_co]:
        """Returns the single element, or null if empty or has more than one element."""
        ...

    @abstractmethod
    def single_predicate(self, predicate: Callable[[T_co], bool]) -> T_co:
        """Returns the single element matching the predicate. Throws if none or more than one match."""
        ...

    @abstractmethod
    def single_or_null_predicate(self, predicate: Callable[[T_co], bool]) -> Optional[T_co]:
        """Returns the single element matching the predicate, or null if none or more than one match."""
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
    # Association operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def associate(self, transform: Callable[[T_co], Tuple[K, V]]) -> 'KotMap[K, V]':
        """Returns a map containing key-value pairs provided by transform function."""
        ...

    @abstractmethod
    def associate_by(self, key_selector: Callable[[T_co], K]) -> 'KotMap[K, T_co]':
        """Returns a map where keys are produced by key_selector applied to elements."""
        ...

    @abstractmethod
    def associate_with(self, value_selector: Callable[[T_co], V]) -> 'KotMap[T_co, V]':
        """Returns a map where elements are keys and values are produced by value_selector."""
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

    # -------------------------------------------------------------------------
    # Additional transformation operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def flat_map_indexed(self, transform: Callable[[int, T_co], Iterable[R]]) -> 'KotList[R]':
        """Returns a single list of all elements yielded from results of transform function with index."""
        ...

    @abstractmethod
    def with_index(self) -> 'KotList[Tuple[int, T_co]]':
        """Returns a list of indexed values (index, element)."""
        ...

    @abstractmethod
    def as_sequence(self) -> Iterator[T_co]:
        """Returns a lazy sequence wrapping this collection."""
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

    # -------------------------------------------------------------------------
    # Element access operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def element_at(self, index: int) -> T_co:
        """Returns an element at the given index. Throws if index is out of bounds."""
        ...

    @abstractmethod
    def element_at_or_else(self, index: int, default_value: Callable[[int], T_co]) -> T_co:
        """Returns an element at the given index or the result of calling defaultValue if out of bounds."""
        ...

    @abstractmethod
    def element_at_or_null(self, index: int) -> Optional[T_co]:
        """Returns an element at the given index or null if the index is out of bounds."""
        ...

    @abstractmethod
    def random(self) -> T_co:
        """Returns a random element. Throws if the collection is empty."""
        ...

    @abstractmethod
    def random_or_null(self) -> Optional[T_co]:
        """Returns a random element, or null if the collection is empty."""
        ...

    # -------------------------------------------------------------------------
    # Search operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def binary_search(self, element: T_co, from_index: int = 0, to_index: Optional[int] = None) -> int:
        """Searches the list for the specified element using the binary search algorithm."""
        ...

    @abstractmethod
    def binary_search_by(self, comparison: Callable[[T_co], int], from_index: int = 0, to_index: Optional[int] = None) -> int:
        """Searches the list using the given comparison function."""
        ...

    @abstractmethod
    def index_of_first(self, predicate: Callable[[T_co], bool]) -> int:
        """Returns the index of the first element matching the predicate, or -1 if not found."""
        ...

    @abstractmethod
    def index_of_last(self, predicate: Callable[[T_co], bool]) -> int:
        """Returns the index of the last element matching the predicate, or -1 if not found."""
        ...

    # -------------------------------------------------------------------------
    # Destructuring operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def component1(self) -> T_co:
        """Returns 1st element from the list."""
        ...

    @abstractmethod
    def component2(self) -> T_co:
        """Returns 2nd element from the list."""
        ...

    @abstractmethod
    def component3(self) -> T_co:
        """Returns 3rd element from the list."""
        ...

    @abstractmethod
    def component4(self) -> T_co:
        """Returns 4th element from the list."""
        ...

    @abstractmethod
    def component5(self) -> T_co:
        """Returns 5th element from the list."""
        ...

    # -------------------------------------------------------------------------
    # Additional transformation operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def as_reversed(self) -> 'KotlinListExtensions[T_co]':
        """Returns a reversed read-only view of the list."""
        ...

    @abstractmethod
    def chunked_transform(self, size: int, transform: Callable[['KotList[T_co]'], R]) -> 'KotList[R]':
        """Splits into chunks and transforms each chunk."""
        ...

    @abstractmethod
    def flatten(self) -> 'KotList[Any]':
        """Returns a single list of all elements from all collections in the given collection."""
        ...

    @abstractmethod
    def slice(self, indices: Iterable[int]) -> 'KotList[T_co]':
        """Returns a list containing elements at the specified indices."""
        ...

    @abstractmethod
    def slice_range(self, range_: range) -> 'KotList[T_co]':
        """Returns a list containing elements at indices in the specified range."""
        ...

    @abstractmethod
    def sorted_with(self, comparator: Callable[[T_co, T_co], int]) -> 'KotList[T_co]':
        """Returns a list sorted according to the specified comparator."""
        ...

    @abstractmethod
    def take_last_while(self, predicate: Callable[[T_co], bool]) -> 'KotList[T_co]':
        """Returns a list containing last elements satisfying the predicate."""
        ...

    @abstractmethod
    def drop_last_while(self, predicate: Callable[[T_co], bool]) -> 'KotList[T_co]':
        """Returns a list containing all elements except last elements satisfying the predicate."""
        ...

    # -------------------------------------------------------------------------
    # Zip transformation operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def zip_transform(self, other: Iterable[R], transform: Callable[[T_co, R], Any]) -> 'KotList[Any]':
        """Returns a list of values built from the elements of this and other using transform."""
        ...

    @abstractmethod
    def zip_with_next_transform(self, transform: Callable[[T_co, T_co], R]) -> 'KotList[R]':
        """Returns a list of results of applying transform to adjacent element pairs."""
        ...

    # -------------------------------------------------------------------------
    # Utility operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def on_each_indexed(self, action: Callable[[int, T_co], None]) -> 'KotlinListExtensions[T_co]':
        """Performs the given action on each element with its index and returns the collection itself."""
        ...

    @abstractmethod
    def first_not_null_of(self, transform: Callable[[T_co], Optional[R]]) -> R:
        """Returns the first non-null value produced by transform. Throws if all are null."""
        ...

    @abstractmethod
    def first_not_null_of_or_null(self, transform: Callable[[T_co], Optional[R]]) -> Optional[R]:
        """Returns the first non-null value produced by transform, or null if all are null."""
        ...

    # -------------------------------------------------------------------------
    # Aggregate operations (List-specific)
    # -------------------------------------------------------------------------

    @abstractmethod
    def max(self) -> T_co:
        """Returns the largest element. Throws if collection is empty."""
        ...

    @abstractmethod
    def min(self) -> T_co:
        """Returns the smallest element. Throws if collection is empty."""
        ...

    @abstractmethod
    def max_by(self, selector: Callable[[T_co], Any]) -> T_co:
        """Returns the first element yielding the largest value. Throws if collection is empty."""
        ...

    @abstractmethod
    def min_by(self, selector: Callable[[T_co], Any]) -> T_co:
        """Returns the first element yielding the smallest value. Throws if collection is empty."""
        ...

    @abstractmethod
    def max_of(self, selector: Callable[[T_co], R]) -> R:
        """Returns the largest value among all values produced by selector. Throws if collection is empty."""
        ...

    @abstractmethod
    def min_of(self, selector: Callable[[T_co], R]) -> R:
        """Returns the smallest value among all values produced by selector. Throws if collection is empty."""
        ...

    @abstractmethod
    def max_of_or_null(self, selector: Callable[[T_co], R]) -> Optional[R]:
        """Returns the largest value among all values produced by selector, or null if empty."""
        ...

    @abstractmethod
    def min_of_or_null(self, selector: Callable[[T_co], R]) -> Optional[R]:
        """Returns the smallest value among all values produced by selector, or null if empty."""
        ...

    @abstractmethod
    def max_of_with(self, comparator: Callable[[R, R], int], selector: Callable[[T_co], R]) -> R:
        """Returns the largest value using the given comparator. Throws if collection is empty."""
        ...

    @abstractmethod
    def min_of_with(self, comparator: Callable[[R, R], int], selector: Callable[[T_co], R]) -> R:
        """Returns the smallest value using the given comparator. Throws if collection is empty."""
        ...

    @abstractmethod
    def max_of_with_or_null(self, comparator: Callable[[R, R], int], selector: Callable[[T_co], R]) -> Optional[R]:
        """Returns the largest value using the given comparator, or null if empty."""
        ...

    @abstractmethod
    def min_of_with_or_null(self, comparator: Callable[[R, R], int], selector: Callable[[T_co], R]) -> Optional[R]:
        """Returns the smallest value using the given comparator, or null if empty."""
        ...

    # -------------------------------------------------------------------------
    # Fold/Reduce operations (List-specific)
    # -------------------------------------------------------------------------

    @abstractmethod
    def fold_indexed(self, initial: R, operation: Callable[[int, R, T_co], R]) -> R:
        """Accumulates value starting with initial, applying operation from left to right with index."""
        ...

    @abstractmethod
    def fold_right(self, initial: R, operation: Callable[[T_co, R], R]) -> R:
        """Accumulates value starting with initial and applying operation from right to left."""
        ...

    @abstractmethod
    def fold_right_indexed(self, initial: R, operation: Callable[[int, T_co, R], R]) -> R:
        """Accumulates value starting with initial, applying operation from right to left with index."""
        ...

    @abstractmethod
    def reduce_indexed(self, operation: Callable[[int, T_co, T_co], T_co]) -> T_co:
        """Accumulates value starting with first element, applying operation from left to right with index."""
        ...

    @abstractmethod
    def reduce_right(self, operation: Callable[[T_co, T_co], T_co]) -> T_co:
        """Accumulates value starting with last element and applying operation from right to left."""
        ...

    @abstractmethod
    def reduce_right_indexed(self, operation: Callable[[int, T_co, T_co], T_co]) -> T_co:
        """Accumulates value starting with last element, applying operation from right to left with index."""
        ...

    @abstractmethod
    def reduce_indexed_or_null(self, operation: Callable[[int, T_co, T_co], T_co]) -> Optional[T_co]:
        """Accumulates value with index or returns null if the collection is empty."""
        ...

    @abstractmethod
    def reduce_right_or_null(self, operation: Callable[[T_co, T_co], T_co]) -> Optional[T_co]:
        """Accumulates value from right to left or returns null if the collection is empty."""
        ...

    @abstractmethod
    def reduce_right_indexed_or_null(self, operation: Callable[[int, T_co, T_co], T_co]) -> Optional[T_co]:
        """Accumulates value from right to left with index or returns null if empty."""
        ...

    # -------------------------------------------------------------------------
    # Running/Scan operations (List-specific)
    # -------------------------------------------------------------------------

    @abstractmethod
    def running_fold(self, initial: R, operation: Callable[[R, T_co], R]) -> 'KotList[R]':
        """Returns a list containing successive accumulation values."""
        ...

    @abstractmethod
    def running_fold_indexed(self, initial: R, operation: Callable[[int, R, T_co], R]) -> 'KotList[R]':
        """Returns a list containing successive accumulation values with index."""
        ...

    @abstractmethod
    def running_reduce(self, operation: Callable[[T_co, T_co], T_co]) -> 'KotList[T_co]':
        """Returns a list containing successive reduction values."""
        ...

    @abstractmethod
    def running_reduce_indexed(self, operation: Callable[[int, T_co, T_co], T_co]) -> 'KotList[T_co]':
        """Returns a list containing successive reduction values with index."""
        ...

    @abstractmethod
    def scan(self, initial: R, operation: Callable[[R, T_co], R]) -> 'KotList[R]':
        """Returns a list containing successive accumulation values (alias for running_fold)."""
        ...

    @abstractmethod
    def scan_indexed(self, initial: R, operation: Callable[[int, R, T_co], R]) -> 'KotList[R]':
        """Returns a list containing successive accumulation values with index."""
        ...

    # -------------------------------------------------------------------------
    # Finding operations (List-specific)
    # -------------------------------------------------------------------------

    @abstractmethod
    def last_predicate(self, predicate: Callable[[T_co], bool]) -> T_co:
        """Returns the last element matching the given predicate. Throws if not found."""
        ...

    @abstractmethod
    def last_or_null_predicate(self, predicate: Callable[[T_co], bool]) -> Optional[T_co]:
        """Returns the last element matching the given predicate, or null if not found."""
        ...

    # -------------------------------------------------------------------------
    # Association operations (List-specific)
    # -------------------------------------------------------------------------

    @abstractmethod
    def associate_by_with_value(self, key_selector: Callable[[T_co], K], value_transform: Callable[[T_co], V]) -> 'KotMap[K, V]':
        """Returns a map where keys and values are produced by the given functions."""
        ...

    @abstractmethod
    def grouping_by(self, key_selector: Callable[[T_co], K]) -> 'Any':
        """Creates a Grouping source from a collection to be used later with grouping operations."""
        ...

    # -------------------------------------------------------------------------
    # Additional List-specific operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def map_indexed_not_null(self, transform: Callable[[int, T_co], Optional[R]]) -> 'KotList[R]':
        """Returns a list containing only the non-null results of applying the indexed transform."""
        ...

    @abstractmethod
    def if_empty(self, default_value: Callable[[], Iterable[T_co]]) -> 'KotlinListExtensions[T_co]':
        """Returns this list if it's not empty, or the result of default_value function."""
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
    # Additional filtering operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def filter_not(self, predicate: Callable[[K, V], bool]) -> 'KotMap[K, V]':
        """Returns a map containing only entries not matching the given predicate."""
        ...

    @abstractmethod
    def filter_not_null(self) -> 'KotMap[K, V]':
        """Returns a map containing only entries with non-null values."""
        ...

    @abstractmethod
    def map_not_null(self, transform: Callable[[K, V], Optional[R]]) -> 'KotList[R]':
        """Returns a list containing only the non-null results of applying the given transform."""
        ...

    # -------------------------------------------------------------------------
    # Aggregate operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def count(self, predicate: Optional[Callable[[K, V], bool]] = None) -> int:
        """Returns the number of entries matching the given predicate, or total count if no predicate."""
        ...

    @abstractmethod
    def max_by(self, selector: Callable[[K, V], Any]) -> Optional[Tuple[K, V]]:
        """Returns the entry yielding the largest value of the given function."""
        ...

    @abstractmethod
    def min_by(self, selector: Callable[[K, V], Any]) -> Optional[Tuple[K, V]]:
        """Returns the entry yielding the smallest value of the given function."""
        ...

    @abstractmethod
    def max_by_or_null(self, selector: Callable[[K, V], Any]) -> Optional[Tuple[K, V]]:
        """Returns the entry yielding the largest value, or null if there are no entries."""
        ...

    @abstractmethod
    def min_by_or_null(self, selector: Callable[[K, V], Any]) -> Optional[Tuple[K, V]]:
        """Returns the entry yielding the smallest value, or null if there are no entries."""
        ...

    # -------------------------------------------------------------------------
    # Conversion operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def to_list(self) -> 'list[Tuple[K, V]]':
        """Returns a Python list containing all key-value pairs."""
        ...

    @abstractmethod
    def to_dict(self) -> 'dict[K, V]':
        """Returns a Python dict containing all key-value pairs."""
        ...

    @abstractmethod
    def to_kot_map(self) -> 'KotMap[K, V]':
        """Returns a KotMap containing all key-value pairs."""
        ...

    @abstractmethod
    def to_kot_mutable_map(self) -> Any:
        """Returns a KotMutableMap containing all key-value pairs."""
        ...

    # -------------------------------------------------------------------------
    # String operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def join_to_string(
        self,
        separator: str = ", ",
        prefix: str = "",
        postfix: str = "",
        limit: int = -1,
        truncated: str = "...",
        transform: Optional[Callable[[K, V], str]] = None
    ) -> str:
        """Creates a string from all the entries separated using separator."""
        ...

    # -------------------------------------------------------------------------
    # Utility operations
    # -------------------------------------------------------------------------

    @abstractmethod
    def with_default(self, default_value: Callable[[K], V]) -> Any:
        """Returns a wrapper of this map having the implicit default value provided."""
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


# =============================================================================
# Pythonic Alias Mixin Interfaces
# =============================================================================

class PythonicIterableExtensionAliases(ABC, Generic[T_co]):
    """Pythonic aliases for KotlinIterableExtensions methods.

    This mixin provides Python-style method names using 'None' instead of 'null'.
    """

    @abstractmethod
    def filter_not_none(self) -> 'KotList[T_co]':
        """Alias for filter_not_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def map_not_none(self, transform: Callable[[T_co], Optional[R]]) -> 'KotList[R]':
        """Alias for map_not_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def max_or_none(self) -> Optional[T_co]:
        """Alias for max_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def min_or_none(self) -> Optional[T_co]:
        """Alias for min_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def max_by_or_none(self, selector: Callable[[T_co], Any]) -> Optional[T_co]:
        """Alias for max_by_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def min_by_or_none(self, selector: Callable[[T_co], Any]) -> Optional[T_co]:
        """Alias for min_by_or_null() - more Pythonic naming."""
        ...


class PythonicListExtensionAliases(PythonicIterableExtensionAliases[T_co]):
    """Pythonic aliases for KotlinListExtensions methods.

    This mixin provides Python-style method names using 'None' instead of 'null'.
    """

    @abstractmethod
    def element_at_or_none(self, index: int) -> Optional[T_co]:
        """Alias for element_at_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def first_or_none_predicate(self, predicate: Callable[[T_co], bool]) -> Optional[T_co]:
        """Alias for first_or_null_predicate() - more Pythonic naming."""
        ...

    @abstractmethod
    def last_or_none_predicate(self, predicate: Callable[[T_co], bool]) -> Optional[T_co]:
        """Alias for last_or_null_predicate() - more Pythonic naming."""
        ...

    @abstractmethod
    def single_or_none(self) -> Optional[T_co]:
        """Alias for single_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def single_or_none_predicate(self, predicate: Callable[[T_co], bool]) -> Optional[T_co]:
        """Alias for single_or_null_predicate() - more Pythonic naming."""
        ...

    @abstractmethod
    def random_or_none(self) -> Optional[T_co]:
        """Alias for random_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def reduce_or_none(self, operation: Callable[[T_co, T_co], T_co]) -> Optional[T_co]:
        """Alias for reduce_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def reduce_indexed_or_none(self, operation: Callable[[int, T_co, T_co], T_co]) -> Optional[T_co]:
        """Alias for reduce_indexed_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def reduce_right_or_none(self, operation: Callable[[T_co, T_co], T_co]) -> Optional[T_co]:
        """Alias for reduce_right_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def reduce_right_indexed_or_none(self, operation: Callable[[int, T_co, T_co], T_co]) -> Optional[T_co]:
        """Alias for reduce_right_indexed_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def map_indexed_not_none(self, transform: Callable[[int, T_co], Optional[R]]) -> 'KotList[R]':
        """Alias for map_indexed_not_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def max_of_or_none(self, selector: Callable[[T_co], R]) -> Optional[R]:
        """Alias for max_of_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def min_of_or_none(self, selector: Callable[[T_co], R]) -> Optional[R]:
        """Alias for min_of_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def max_of_with_or_none(self, comparator: Callable[[R, R], int], selector: Callable[[T_co], R]) -> Optional[R]:
        """Alias for max_of_with_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def min_of_with_or_none(self, comparator: Callable[[R, R], int], selector: Callable[[T_co], R]) -> Optional[R]:
        """Alias for min_of_with_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def first_not_none_of(self, transform: Callable[[T_co], Optional[R]]) -> R:
        """Alias for first_not_null_of() - more Pythonic naming."""
        ...

    @abstractmethod
    def first_not_none_of_or_none(self, transform: Callable[[T_co], Optional[R]]) -> Optional[R]:
        """Alias for first_not_null_of_or_null() - more Pythonic naming."""
        ...


class PythonicMutableListAliases(ABC, Generic[T_co]):
    """Pythonic aliases for KotlinMutableList methods.

    This mixin provides Python-style method names using 'None' instead of 'null'.
    """

    @abstractmethod
    def remove_first_or_none(self) -> Optional[T_co]:
        """Alias for remove_first_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def remove_last_or_none(self) -> Optional[T_co]:
        """Alias for remove_last_or_null() - more Pythonic naming."""
        ...


class PythonicMapExtensionAliases(ABC, Generic[K, V]):
    """Pythonic aliases for KotlinMapExtensions methods.

    This mixin provides Python-style method names using 'None' instead of 'null'.
    """

    @abstractmethod
    def get_or_none(self, key: K) -> Optional[V]:
        """Alias for get_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def filter_not_none(self) -> 'KotMap[K, V]':
        """Alias for filter_not_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def map_not_none(self, transform: Callable[[K, V], Optional[R]]) -> 'KotList[R]':
        """Alias for map_not_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def max_by_or_none(self, selector: Callable[[K, V], Any]) -> Optional[Tuple[K, V]]:
        """Alias for max_by_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def min_by_or_none(self, selector: Callable[[K, V], Any]) -> Optional[Tuple[K, V]]:
        """Alias for min_by_or_null() - more Pythonic naming."""
        ...


class PythonicSetAliases(ABC, Generic[T_co]):
    """Pythonic aliases for KotSet methods.

    This mixin provides Python-style method names using 'None' instead of 'null'.
    """

    @abstractmethod
    def first_or_none(self) -> Optional[T_co]:
        """Alias for first_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def first_or_none_predicate(self, predicate: Callable[[T_co], bool]) -> Optional[T_co]:
        """Alias for first_or_null_predicate() - more Pythonic naming."""
        ...

    @abstractmethod
    def last_or_none(self) -> Optional[T_co]:
        """Alias for last_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def single_or_none(self) -> Optional[T_co]:
        """Alias for single_or_null() - more Pythonic naming."""
        ...

    @abstractmethod
    def single_or_none_predicate(self, predicate: Callable[[T_co], bool]) -> Optional[T_co]:
        """Alias for single_or_null_predicate() - more Pythonic naming."""
        ...

    @abstractmethod
    def reduce_or_none(self, operation: Callable[[T_co, T_co], T_co]) -> Optional[T_co]:
        """Alias for reduce_or_null() - more Pythonic naming."""
        ...
