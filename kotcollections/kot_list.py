from typing import TypeVar, Generic, Callable, Optional, List, Tuple, Iterator, Any, Set, Dict, Union
from collections.abc import Iterable
import random
import bisect
from functools import reduce

T = TypeVar('T')
R = TypeVar('R')
K = TypeVar('K')
V = TypeVar('V')


class KotList(Generic[T]):
    def __init__(self, elements: Optional[Iterable[T]] = None):
        self._element_type: Optional[type] = None
        if elements is None:
            self._elements: List[T] = []
        else:
            elements_list = list(elements)
            if elements_list:
                # Set the element type based on the first element
                first_elem = elements_list[0]
                if isinstance(first_elem, KotList):
                    self._element_type = KotList
                else:
                    self._element_type = type(first_elem)
                
                # Check all elements have the same type
                for elem in elements_list:
                    self._check_type(elem)
            
            self._elements = elements_list
    
    def _check_type(self, element: Any) -> None:
        """Check if the element has the correct type for this list."""
        if self._element_type is None:
            # First element sets the type
            if isinstance(element, KotList):
                self._element_type = KotList
            else:
                self._element_type = type(element)
        else:
            # Type check: allow T type or KotList type
            if isinstance(element, KotList):
                if self._element_type != KotList:
                    raise TypeError(f"Cannot add KotList to KotList[{self._element_type.__name__}]")
            elif type(element) != self._element_type:
                raise TypeError(f"Cannot add element of type '{type(element).__name__}' to KotList[{self._element_type.__name__}]")
    
    def __repr__(self) -> str:
        return f"KotList({self._elements})"
    
    def __str__(self) -> str:
        return str(self._elements)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KotList):
            return False
        return self._elements == other._elements
    
    def __hash__(self) -> int:
        return hash(tuple(self._elements))
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._elements)
    
    def __getitem__(self, index: int) -> T:
        return self.get(index)
    
    def __len__(self) -> int:
        return self.size
    
    @property
    def size(self) -> int:
        return len(self._elements)
    
    @property
    def indices(self) -> range:
        return range(self.size)
    
    @property
    def last_index(self) -> int:
        return self.size - 1 if self.size > 0 else -1
    
    def is_empty(self) -> bool:
        return self.size == 0
    
    def is_not_empty(self) -> bool:
        return self.size > 0
    
    def get(self, index: int) -> T:
        if not 0 <= index < self.size:
            raise IndexError(f"Index {index} out of bounds for list of size {self.size}")
        return self._elements[index]
    
    def get_or_null(self, index: int) -> Optional[T]:
        return self._elements[index] if 0 <= index < self.size else None
    
    def get_or_else(self, index: int, default_value: Callable[[int], T]) -> T:
        return self._elements[index] if 0 <= index < self.size else default_value(index)
    
    def first(self) -> T:
        if self.is_empty():
            raise IndexError("List is empty")
        return self._elements[0]
    
    def first_predicate(self, predicate: Callable[[T], bool]) -> T:
        for element in self._elements:
            if predicate(element):
                return element
        raise ValueError("No element matching predicate found")
    
    def first_or_null(self) -> Optional[T]:
        return self._elements[0] if self.is_not_empty() else None
    
    def first_or_null_predicate(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for element in self._elements:
            if predicate(element):
                return element
        return None
    
    def last(self) -> T:
        if self.is_empty():
            raise IndexError("List is empty")
        return self._elements[-1]
    
    def last_predicate(self, predicate: Callable[[T], bool]) -> T:
        for element in reversed(self._elements):
            if predicate(element):
                return element
        raise ValueError("No element matching predicate found")
    
    def last_or_null(self) -> Optional[T]:
        return self._elements[-1] if self.is_not_empty() else None
    
    def last_or_null_predicate(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for element in reversed(self._elements):
            if predicate(element):
                return element
        return None
    
    def element_at(self, index: int) -> T:
        return self.get(index)
    
    def element_at_or_else(self, index: int, default_value: Callable[[int], T]) -> T:
        return self.get_or_else(index, default_value)
    
    def element_at_or_null(self, index: int) -> Optional[T]:
        return self.get_or_null(index)
    
    def contains(self, element: T) -> bool:
        return element in self._elements
    
    def contains_all(self, elements: Iterable[T]) -> bool:
        elements_set = set(elements)
        return all(elem in self._elements for elem in elements_set)
    
    def index_of(self, element: T) -> int:
        try:
            return self._elements.index(element)
        except ValueError:
            return -1
    
    def last_index_of(self, element: T) -> int:
        for i in range(len(self._elements) - 1, -1, -1):
            if self._elements[i] == element:
                return i
        return -1
    
    def index_of_first(self, predicate: Callable[[T], bool]) -> int:
        for i, element in enumerate(self._elements):
            if predicate(element):
                return i
        return -1
    
    def index_of_last(self, predicate: Callable[[T], bool]) -> int:
        for i in range(len(self._elements) - 1, -1, -1):
            if predicate(self._elements[i]):
                return i
        return -1
    
    def binary_search(self, element: T, comparator: Optional[Callable[[T, T], int]] = None) -> int:
        if comparator is None:
            index = bisect.bisect_left(self._elements, element)
            if index < len(self._elements) and self._elements[index] == element:
                return index
            return -(index + 1)
        else:
            left, right = 0, len(self._elements) - 1
            while left <= right:
                mid = (left + right) // 2
                cmp = comparator(self._elements[mid], element)
                if cmp < 0:
                    left = mid + 1
                elif cmp > 0:
                    right = mid - 1
                else:
                    return mid
            return -(left + 1)
    
    def map(self, transform: Callable[[T], R]) -> 'KotList[R]':
        return KotList([transform(element) for element in self._elements])
    
    def map_indexed(self, transform: Callable[[int, T], R]) -> 'KotList[R]':
        return KotList([transform(i, element) for i, element in enumerate(self._elements)])
    
    def map_not_null(self, transform: Callable[[T], Optional[R]]) -> 'KotList[R]':
        result = []
        for element in self._elements:
            transformed = transform(element)
            if transformed is not None:
                result.append(transformed)
        return KotList(result)
    
    def flat_map(self, transform: Callable[[T], Iterable[R]]) -> 'KotList[R]':
        result = []
        for element in self._elements:
            result.extend(transform(element))
        return KotList(result)
    
    def flatten(self) -> 'KotList[Any]':
        result = []
        for element in self._elements:
            if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
                result.extend(element)
            else:
                result.append(element)
        return KotList(result)
    
    def associate_with(self, value_selector: Callable[[T], V]) -> Dict[T, V]:
        return {element: value_selector(element) for element in self._elements}
    
    def associate_by(self, key_selector: Callable[[T], K]) -> Dict[K, T]:
        result = {}
        for element in self._elements:
            result[key_selector(element)] = element
        return result
    
    def associate_by_with_value(self, key_selector: Callable[[T], K], 
                                value_transform: Callable[[T], V]) -> Dict[K, V]:
        result = {}
        for element in self._elements:
            result[key_selector(element)] = value_transform(element)
        return result
    
    def filter(self, predicate: Callable[[T], bool]) -> 'KotList[T]':
        return KotList([element for element in self._elements if predicate(element)])
    
    def filter_indexed(self, predicate: Callable[[int, T], bool]) -> 'KotList[T]':
        return KotList([element for i, element in enumerate(self._elements) if predicate(i, element)])
    
    def filter_not(self, predicate: Callable[[T], bool]) -> 'KotList[T]':
        return KotList([element for element in self._elements if not predicate(element)])
    
    def filter_not_null(self) -> 'KotList[T]':
        return KotList([element for element in self._elements if element is not None])
    
    def filter_is_instance(self, klass: type) -> 'KotList[Any]':
        return KotList([element for element in self._elements if isinstance(element, klass)])
    
    def partition(self, predicate: Callable[[T], bool]) -> Tuple['KotList[T]', 'KotList[T]']:
        matching = []
        non_matching = []
        for element in self._elements:
            if predicate(element):
                matching.append(element)
            else:
                non_matching.append(element)
        return KotList(matching), KotList(non_matching)
    
    def any(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        if predicate is None:
            return self.is_not_empty()
        return any(predicate(element) for element in self._elements)
    
    def all(self, predicate: Callable[[T], bool]) -> bool:
        return all(predicate(element) for element in self._elements)
    
    def none(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        if predicate is None:
            return self.is_empty()
        return not any(predicate(element) for element in self._elements)
    
    def count(self, predicate: Optional[Callable[[T], bool]] = None) -> int:
        if predicate is None:
            return self.size
        return sum(1 for element in self._elements if predicate(element))
    
    def sum_of(self, selector: Callable[[T], Union[int, float]]) -> Union[int, float]:
        return sum(selector(element) for element in self._elements)
    
    def max_or_null(self) -> Optional[T]:
        return max(self._elements) if self.is_not_empty() else None
    
    def min_or_null(self) -> Optional[T]:
        return min(self._elements) if self.is_not_empty() else None
    
    def max_by_or_null(self, selector: Callable[[T], Any]) -> Optional[T]:
        if self.is_empty():
            return None
        return max(self._elements, key=selector)
    
    def min_by_or_null(self, selector: Callable[[T], Any]) -> Optional[T]:
        if self.is_empty():
            return None
        return min(self._elements, key=selector)
    
    def average(self) -> float:
        if self.is_empty():
            raise ValueError("Cannot compute average of empty list")
        return sum(self._elements) / self.size
    
    def sorted(self, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> 'KotList[T]':
        return KotList(sorted(self._elements, key=key, reverse=reverse))
    
    def sorted_descending(self) -> 'KotList[T]':
        return KotList(sorted(self._elements, reverse=True))
    
    def sorted_by(self, selector: Callable[[T], Any]) -> 'KotList[T]':
        return KotList(sorted(self._elements, key=selector))
    
    def sorted_by_descending(self, selector: Callable[[T], Any]) -> 'KotList[T]':
        return KotList(sorted(self._elements, key=selector, reverse=True))
    
    def reversed(self) -> 'KotList[T]':
        return KotList(reversed(self._elements))
    
    def shuffled(self, random_instance: Optional[random.Random] = None) -> 'KotList[T]':
        elements_copy = self._elements.copy()
        if random_instance:
            random_instance.shuffle(elements_copy)
        else:
            random.shuffle(elements_copy)
        return KotList(elements_copy)
    
    def group_by(self, key_selector: Callable[[T], K]) -> Dict[K, 'KotList[T]']:
        result: Dict[K, List[T]] = {}
        for element in self._elements:
            key = key_selector(element)
            if key not in result:
                result[key] = []
            result[key].append(element)
        return {k: KotList(v) for k, v in result.items()}
    
    def group_by_with_value(self, key_selector: Callable[[T], K], 
                            value_transform: Callable[[T], V]) -> Dict[K, 'KotList[V]']:
        result: Dict[K, List[V]] = {}
        for element in self._elements:
            key = key_selector(element)
            if key not in result:
                result[key] = []
            result[key].append(value_transform(element))
        return {k: KotList(v) for k, v in result.items()}
    
    def chunked(self, size: int) -> 'KotList[KotList[T]]':
        if size <= 0:
            raise ValueError("Size must be positive")
        chunks = []
        for i in range(0, len(self._elements), size):
            chunks.append(KotList(self._elements[i:i + size]))
        return KotList(chunks)
    
    def chunked_transform(self, size: int, transform: Callable[['KotList[T]'], R]) -> 'KotList[R]':
        if size <= 0:
            raise ValueError("Size must be positive")
        result = []
        for i in range(0, len(self._elements), size):
            chunk = KotList(self._elements[i:i + size])
            result.append(transform(chunk))
        return KotList(result)
    
    def windowed(self, size: int, step: int = 1, partial_windows: bool = False) -> 'KotList[KotList[T]]':
        if size <= 0 or step <= 0:
            raise ValueError("Size and step must be positive")
        windows = []
        for i in range(0, len(self._elements), step):
            window = self._elements[i:i + size]
            if len(window) == size or (partial_windows and window):
                windows.append(KotList(window))
            elif not partial_windows and len(window) < size:
                break
        return KotList(windows)
    
    def distinct(self) -> 'KotList[T]':
        seen = set()
        result = []
        for element in self._elements:
            if element not in seen:
                seen.add(element)
                result.append(element)
        return KotList(result)
    
    def distinct_by(self, selector: Callable[[T], K]) -> 'KotList[T]':
        seen = set()
        result = []
        for element in self._elements:
            key = selector(element)
            if key not in seen:
                seen.add(key)
                result.append(element)
        return KotList(result)
    
    def intersect(self, other: Iterable[T]) -> 'KotList[T]':
        other_set = set(other)
        return KotList([element for element in self._elements if element in other_set])
    
    def union(self, other: Iterable[T]) -> 'KotList[T]':
        result = list(self._elements)
        seen = set(self._elements)
        for element in other:
            if element not in seen:
                result.append(element)
                seen.add(element)
        return KotList(result)
    
    def plus(self, element: Union[T, Iterable[T]]) -> 'KotList[T]':
        if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
            return KotList(self._elements + list(element))
        else:
            return KotList(self._elements + [element])
    
    def minus(self, element: Union[T, Iterable[T]]) -> 'KotList[T]':
        if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
            to_remove = set(element)
            return KotList([e for e in self._elements if e not in to_remove])
        else:
            result = self._elements.copy()
            if element in result:
                result.remove(element)
            return KotList(result)
    
    def sub_list(self, from_index: int, to_index: int) -> 'KotList[T]':
        return KotList(self._elements[from_index:to_index])
    
    def zip(self, other: Iterable[R]) -> 'KotList[Tuple[T, R]]':
        return KotList(list(zip(self._elements, other)))
    
    def zip_transform(self, other: Iterable[R], transform: Callable[[T, R], V]) -> 'KotList[V]':
        return KotList([transform(a, b) for a, b in zip(self._elements, other)])
    
    def unzip(self) -> Tuple['KotList[Any]', 'KotList[Any]']:
        if self.is_empty():
            return KotList(), KotList()
        first_elements = []
        second_elements = []
        for pair in self._elements:
            first_elements.append(pair[0])
            second_elements.append(pair[1])
        return KotList(first_elements), KotList(second_elements)
    
    def fold(self, initial: R, operation: Callable[[R, T], R]) -> R:
        result = initial
        for element in self._elements:
            result = operation(result, element)
        return result
    
    def reduce(self, operation: Callable[[T, T], T]) -> T:
        if self.is_empty():
            raise ValueError("Cannot reduce empty list")
        return reduce(operation, self._elements)
    
    def scan(self, initial: R, operation: Callable[[R, T], R]) -> 'KotList[R]':
        result = [initial]
        acc = initial
        for element in self._elements:
            acc = operation(acc, element)
            result.append(acc)
        return KotList(result)
    
    def for_each(self, action: Callable[[T], None]) -> None:
        for element in self._elements:
            action(element)
    
    def for_each_indexed(self, action: Callable[[int, T], None]) -> None:
        for i, element in enumerate(self._elements):
            action(i, element)
    
    def on_each(self, action: Callable[[T], None]) -> 'KotList[T]':
        for element in self._elements:
            action(element)
        return self
    
    def to_list(self) -> List[T]:
        return self._elements.copy()
    
    def to_mutable_list(self) -> 'KotMutableList[T]':
        from .kot_mutable_list import KotMutableList
        return KotMutableList(self._elements)
    
    def to_set(self) -> Set[T]:
        return set(self._elements)
    
    def to_mutable_set(self) -> Set[T]:
        return set(self._elements)
    
    def join_to_string(self, separator: str = ", ", prefix: str = "", postfix: str = "",
                       limit: int = -1, truncated: str = "...", 
                       transform: Optional[Callable[[T], str]] = None) -> str:
        if transform is None:
            transform = str
        
        result = prefix
        count = 0
        
        for i, element in enumerate(self._elements):
            if limit >= 0 and count >= limit:
                result += truncated
                break
            
            if i > 0:
                result += separator
            
            result += transform(element)
            count += 1
        
        result += postfix
        return result