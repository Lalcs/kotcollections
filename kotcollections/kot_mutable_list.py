from __future__ import annotations

import random
from functools import cmp_to_key
from typing import TypeVar, Optional, Callable, Iterable, List, Type

from kotcollections.kot_list import KotList
from kotcollections.interfaces import KotlinMutableList

T = TypeVar('T')


class MutableListIterator:
    """A bidirectional iterator over a mutable list that supports element removal, addition, and modification.

    This iterator allows traversing the list in both directions, and provides methods to modify
    the list during iteration.
    """

    def __init__(self, mutable_list: 'KotMutableList[T]', index: int = 0):
        """Initialize a MutableListIterator.

        Args:
            mutable_list: The KotMutableList to iterate over
            index: The starting index (default: 0)

        Raises:
            IndexError: If index is out of bounds
        """
        if index < 0 or index > mutable_list.size:
            raise IndexError(f"Index {index} out of bounds for list of size {mutable_list.size}")
        self._list = mutable_list
        self._cursor = index
        self._last_returned = -1

    def has_next(self) -> bool:
        """Returns true if the iteration has more elements when traversing forward."""
        return self._cursor < self._list.size

    def next(self) -> T:
        """Returns the next element in the iteration and advances the iterator position.

        Raises:
            StopIteration: If there are no more elements
        """
        if not self.has_next():
            raise StopIteration("No more elements")
        element = self._list._elements[self._cursor]
        self._last_returned = self._cursor
        self._cursor += 1
        return element

    def has_previous(self) -> bool:
        """Returns true if the iteration has more elements when traversing backward."""
        return self._cursor > 0

    def previous(self) -> T:
        """Returns the previous element in the iteration and moves the iterator position backward.

        Raises:
            StopIteration: If there are no previous elements
        """
        if not self.has_previous():
            raise StopIteration("No previous elements")
        self._cursor -= 1
        element = self._list._elements[self._cursor]
        self._last_returned = self._cursor
        return element

    def next_index(self) -> int:
        """Returns the index of the element that would be returned by a subsequent call to next()."""
        return self._cursor

    def previous_index(self) -> int:
        """Returns the index of the element that would be returned by a subsequent call to previous()."""
        return self._cursor - 1

    def add(self, element: T) -> None:
        """Inserts the specified element into the list at the current cursor position.

        The element is inserted immediately before the element that would be returned by next(),
        if any, and after the element that would be returned by previous(), if any.

        Args:
            element: The element to add
        """
        self._list.add_at(self._cursor, element)
        self._cursor += 1
        self._last_returned = -1

    def remove(self) -> None:
        """Removes from the list the last element that was returned by next() or previous().

        This call can only be made once per call to next() or previous().

        Raises:
            RuntimeError: If neither next() nor previous() have been called,
                         or if remove() or add() have been called after the last call to next() or previous()
        """
        if self._last_returned < 0:
            raise RuntimeError("No element to remove (call next() or previous() first)")

        self._list.remove_at(self._last_returned)

        if self._last_returned < self._cursor:
            self._cursor -= 1

        self._last_returned = -1

    def set(self, element: T) -> None:
        """Replaces the last element returned by next() or previous() with the specified element.

        This call can only be made if neither remove() nor add() have been called after
        the last call to next() or previous().

        Args:
            element: The element to replace the last returned element with

        Raises:
            RuntimeError: If neither next() nor previous() have been called,
                         or if remove() or add() have been called after the last call to next() or previous()
        """
        if self._last_returned < 0:
            raise RuntimeError("No element to set (call next() or previous() first)")

        self._list.set(self._last_returned, element)

    def __iter__(self):
        """Returns self as an iterator."""
        return self

    def __next__(self) -> T:
        """Python iterator protocol - calls next()."""
        return self.next()


class KotMutableList(KotList[T], KotlinMutableList[T]):
    def __init__(self, elements: Optional[Iterable[T]] = None):
        super().__init__(elements)

    @classmethod
    def __class_getitem__(cls, element_type: Type[T]) -> Type['KotMutableList[T]']:
        """Enable KotMutableList[Type]() syntax for type specification.

        Example:
            animals = KotMutableList[Animal]()
            animals.add(Dog("Buddy"))
            animals.add(Cat("Whiskers"))
        """
        class TypedKotMutableList(cls):
            def __init__(self, elements=None):
                # Only set element type if it's an actual type, not a type variable
                if isinstance(element_type, type):
                    self._element_type = element_type
                else:
                    self._element_type = None
                self._elements = []
                # Now process elements with the correct type set
                if elements is not None:
                    for elem in elements:
                        self._check_type(elem)
                        self._elements.append(elem)

        # Set a meaningful name for debugging (handle cases where __name__ might not exist)
        type_name = getattr(element_type, '__name__', str(element_type))
        TypedKotMutableList.__name__ = f"{cls.__name__}[{type_name}]"
        TypedKotMutableList.__qualname__ = f"{cls.__qualname__}[{type_name}]"

        return TypedKotMutableList

    @classmethod
    def of_type(cls, element_type: Type[T], elements: Optional[Iterable[T]] = None) -> 'KotMutableList[T]':
        """Create a KotMutableList with a specific element type.

        This method is particularly useful when you want to create a mutable list of a parent type
        but only have instances of child types. It enables runtime type checking to ensure
        all elements are instances of the specified type or its subclasses.

        Type Checking Behavior:
            - Accepts exact type matches (Dog instance in Dog list)
            - Accepts subclass instances (Dog instance in Animal list)
            - Rejects parent class instances (Animal instance in Dog list)
            - Rejects unrelated types (Cat instance in Dog list)

        Args:
            element_type: The type of elements this list will contain. All elements
                         must be instances of this type or its subclasses.
            elements: Optional initial elements. Each element will be type-checked.

        Returns:
            A new KotMutableList instance with the specified element type

        Raises:
            TypeError: If any element in `elements` is not an instance of `element_type`

        Examples:
            >>> # Create empty typed list
            >>> animals = KotMutableList.of_type(Animal)

            >>> # Create with mixed subclass instances and add more
            >>> animals = KotMutableList.of_type(Animal, [Dog("Buddy")])
            >>> animals.add(Cat("Whiskers"))  # Type-checked at runtime
        """
        # Use __class_getitem__ to create the same dynamic subclass
        typed_class = cls[element_type]
        return typed_class(elements)

    def __setitem__(self, index: int, value: T) -> None:
        self.set(index, value)

    def __delitem__(self, index: int) -> None:
        self.remove_at(index)

    def add(self, element: T) -> bool:
        self._check_type(element)
        self._elements.append(element)
        return True

    def add_at(self, index: int, element: T) -> None:
        if not 0 <= index <= self.size:
            raise IndexError(f"Index {index} out of bounds for insertion")
        self._check_type(element)
        self._elements.insert(index, element)

    def add_all(self, elements: Iterable[T]) -> bool:
        elements_list = list(elements)
        if elements_list:
            for element in elements_list:
                self._check_type(element)
            self._elements.extend(elements_list)
            return True
        return False

    def add_all_at(self, index: int, elements: Iterable[T]) -> bool:
        if not 0 <= index <= self.size:
            raise IndexError(f"Index {index} out of bounds for insertion")
        elements_list = list(elements)
        if elements_list:
            for element in elements_list:
                self._check_type(element)
            for i, element in enumerate(elements_list):
                self._elements.insert(index + i, element)
            return True
        return False

    def set(self, index: int, element: T) -> T:
        if not 0 <= index < self.size:
            raise IndexError(f"Index {index} out of bounds for list of size {self.size}")
        self._check_type(element)
        old_element = self._elements[index]
        self._elements[index] = element
        return old_element

    def remove_at(self, index: int) -> T:
        if not 0 <= index < self.size:
            raise IndexError(f"Index {index} out of bounds for list of size {self.size}")
        return self._elements.pop(index)

    def remove(self, element: T) -> bool:
        try:
            self._elements.remove(element)
            return True
        except ValueError:
            return False

    def remove_all(self, elements: Iterable[T]) -> bool:
        elements_set = set(elements)
        initial_size = self.size
        self._elements = [e for e in self._elements if e not in elements_set]
        return self.size < initial_size

    def remove_first(self) -> T:
        """Removes the first element from this mutable list."""
        if self.is_empty():
            raise IndexError("List is empty")
        return self._elements.pop(0)

    def remove_last(self) -> T:
        """Removes the last element from this mutable list."""
        if self.is_empty():
            raise IndexError("List is empty")
        return self._elements.pop()

    def remove_first_or_null(self) -> Optional[T]:
        """Removes the first element from this mutable list and returns it, or null if the list is empty."""
        if self.is_empty():
            return None
        return self._elements.pop(0)

    def remove_first_or_none(self) -> Optional[T]:
        """Alias for remove_first_or_null() - more Pythonic naming."""
        return self.remove_first_or_null()

    def remove_last_or_null(self) -> Optional[T]:
        """Removes the last element from this mutable list and returns it, or null if the list is empty."""
        if self.is_empty():
            return None
        return self._elements.pop()

    def remove_last_or_none(self) -> Optional[T]:
        """Alias for remove_last_or_null() - more Pythonic naming."""
        return self.remove_last_or_null()

    def retain_all(self, elements: Iterable[T]) -> bool:
        elements_set = set(elements)
        initial_size = self.size
        self._elements = [e for e in self._elements if e in elements_set]
        return self.size < initial_size

    def remove_if(self, filter_predicate: Callable[[T], bool]) -> bool:
        """Removes all elements that satisfy the given predicate. Returns true if any elements were removed."""
        initial_size = self.size
        self._elements = [e for e in self._elements if not filter_predicate(e)]
        return self.size < initial_size

    def replace_all(self, operator: Callable[[T], T]) -> None:
        """Replaces each element of this list with the result of applying the operator to that element."""
        for i in range(self.size):
            new_element = operator(self._elements[i])
            self._check_type(new_element)
            self._elements[i] = new_element

    def clear(self) -> None:
        self._elements.clear()

    def sort(self, key: Optional[Callable[[T], any]] = None, reverse: bool = False) -> None:
        self._elements.sort(key=key, reverse=reverse)

    def sort_descending(self) -> None:
        self._elements.sort(reverse=True)

    def sort_by(self, selector: Callable[[T], any]) -> None:
        self._elements.sort(key=selector)

    def sort_by_descending(self, selector: Callable[[T], any]) -> None:
        self._elements.sort(key=selector, reverse=True)

    def sort_with(self, comparator: Callable[[T, T], int]) -> None:
        """Sorts elements in the list in-place according to the specified comparator."""
        self._elements.sort(key=cmp_to_key(comparator))

    def reverse(self) -> None:
        self._elements.reverse()

    def shuffle(self, random_instance: Optional[random.Random] = None) -> None:
        if random_instance:
            random_instance.shuffle(self._elements)
        else:
            random.shuffle(self._elements)

    def fill(self, value: T) -> None:
        for i in range(self.size):
            self._elements[i] = value

    def as_reversed(self) -> 'KotMutableList[T]':
        class KotReversedMutableList(KotMutableList[T]):
            def __init__(self, original: KotMutableList[T]):
                self._original = original
                super().__init__()

            @property
            def _elements(self) -> List[T]:
                return list(reversed(self._original._elements))

            @_elements.setter
            def _elements(self, value: List[T]) -> None:
                pass

            def __getitem__(self, index: int) -> T:
                return self._original._elements[self._original.size - 1 - index]

            def __setitem__(self, index: int, value: T) -> None:
                self._original._elements[self._original.size - 1 - index] = value

            def __len__(self) -> int:
                return self._original.size

        return KotReversedMutableList(self)

    def list_iterator(self, index: int = 0) -> MutableListIterator:
        """Returns a mutable list iterator over the elements in this list, starting at the specified index.

        Args:
            index: The index to start iterating from (default: 0)

        Returns:
            A MutableListIterator positioned at the specified index

        Raises:
            IndexError: If index is out of bounds

        Examples:
            >>> lst = KotMutableList([1, 2, 3, 4, 5])
            >>> it = lst.list_iterator()
            >>> it.next()  # Returns 1
            1
            >>> it.next()  # Returns 2
            2
            >>> it.previous()  # Returns 2
            2
            >>> it.add(10)  # Inserts 10 at current position
            >>> lst.to_list()
            [1, 10, 2, 3, 4, 5]
        """
        return MutableListIterator(self, index)

    def sub_list(self, from_index: int, to_index: int) -> 'KotMutableList[T]':
        """Returns a view of the portion of this list between the specified fromIndex (inclusive) and toIndex (exclusive).

        The returned list is backed by this list, so changes in the returned list are reflected in this list,
        and vice-versa.

        Args:
            from_index: Low endpoint (inclusive) of the subList
            to_index: High endpoint (exclusive) of the subList

        Returns:
            A view of the specified range within this list

        Raises:
            IndexError: If from_index or to_index is out of bounds, or if from_index > to_index

        Examples:
            >>> lst = KotMutableList([1, 2, 3, 4, 5])
            >>> sub = lst.sub_list(1, 4)
            >>> sub.to_list()
            [2, 3, 4]
            >>> sub.set(0, 10)  # Modifies the original list
            10
            >>> lst.to_list()
            [1, 10, 3, 4, 5]
        """
        if from_index < 0 or to_index > self.size:
            raise IndexError(f"fromIndex {from_index} or toIndex {to_index} out of bounds for list of size {self.size}")
        if from_index > to_index:
            raise IndexError(f"fromIndex {from_index} > toIndex {to_index}")

        class KotMutableSubList(KotMutableList[T]):
            def __init__(self, parent: 'KotMutableList[T]', start: int, end: int):
                self._parent = parent
                self._start = start
                self._end = end
                # Don't call super().__init__() to avoid creating separate _elements

            @property
            def _elements(self) -> List[T]:
                """Return a view of the parent's elements."""
                return self._parent._elements[self._start:self._end]

            @_elements.setter
            def _elements(self, value: List[T]) -> None:
                """Update the parent's elements."""
                self._parent._elements[self._start:self._end] = value
                self._end = self._start + len(value)

            @property
            def size(self) -> int:
                """Return the size of the sublist."""
                return self._end - self._start

            def __getitem__(self, index: int) -> T:
                if not 0 <= index < self.size:
                    raise IndexError(f"Index {index} out of bounds for sublist of size {self.size}")
                return self._parent._elements[self._start + index]

            def __setitem__(self, index: int, value: T) -> None:
                if not 0 <= index < self.size:
                    raise IndexError(f"Index {index} out of bounds for sublist of size {self.size}")
                self._parent._check_type(value)
                self._parent._elements[self._start + index] = value

            def __delitem__(self, index: int) -> None:
                if not 0 <= index < self.size:
                    raise IndexError(f"Index {index} out of bounds for sublist of size {self.size}")
                del self._parent._elements[self._start + index]
                self._end -= 1

            def add(self, element: T) -> bool:
                self._parent._check_type(element)
                self._parent._elements.insert(self._end, element)
                self._end += 1
                return True

            def add_at(self, index: int, element: T) -> None:
                if not 0 <= index <= self.size:
                    raise IndexError(f"Index {index} out of bounds for insertion in sublist of size {self.size}")
                self._parent._check_type(element)
                self._parent._elements.insert(self._start + index, element)
                self._end += 1

            def set(self, index: int, element: T) -> T:
                """Set element at the specified index in the sublist."""
                if not 0 <= index < self.size:
                    raise IndexError(f"Index {index} out of bounds for sublist of size {self.size}")
                self._parent._check_type(element)
                old_element = self._parent._elements[self._start + index]
                self._parent._elements[self._start + index] = element
                return old_element

            def remove_at(self, index: int) -> T:
                if not 0 <= index < self.size:
                    raise IndexError(f"Index {index} out of bounds for sublist of size {self.size}")
                element = self._parent._elements.pop(self._start + index)
                self._end -= 1
                return element

            def clear(self) -> None:
                del self._parent._elements[self._start:self._end]
                self._end = self._start

            def _check_type(self, element: T) -> None:
                """Delegate type checking to parent."""
                self._parent._check_type(element)

        return KotMutableSubList(self, from_index, to_index)
