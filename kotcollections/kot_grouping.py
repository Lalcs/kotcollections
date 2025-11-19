from typing import TypeVar, Generic, Callable, Dict, List, Optional

T = TypeVar('T')
K = TypeVar('K')
R = TypeVar('R')


class KotGrouping(Generic[T, K]):
    """Represents a source of elements with a keyOf function, which can be applied to each element to get its key.

    A Grouping structure serves as an intermediate step in group-and-fold operations:
    they group elements by their keys and then fold each group with some aggregating operation.

    Grouping is created from a collection of elements using the groupingBy() method on collections.

    Example:
        >>> lst = KotList(["apple", "apricot", "banana", "cherry", "avocado"])
        >>> grouping = lst.groupingBy(lambda s: s[0])
        >>> grouping.eachCount()  # Returns KotMap({'a': 3, 'b': 1, 'c': 1})
    """

    def __init__(self, source: List[T], key_selector: Callable[[T], K]):
        """Initialize a Grouping instance.

        Args:
            source: The source collection of elements
            key_selector: A function that extracts the key from an element
        """
        self._source = source
        self._key_selector = key_selector

    def _group_by_key(self) -> Dict[K, List[T]]:
        """Internal method to group elements by their keys.

        Returns:
            A dictionary mapping keys to lists of elements
        """
        groups: Dict[K, List[T]] = {}
        for element in self._source:
            key = self._key_selector(element)
            if key not in groups:
                groups[key] = []
            groups[key].append(element)
        return groups

    def each_count(self) -> 'KotMap[K, int]':
        """Groups elements from the Grouping source by key and counts elements in each group.

        Returns:
            A KotMap associating the key of each group with the count of elements in the group.

        Examples:
            >>> lst = KotList(["apple", "apricot", "banana", "cherry", "avocado"])
            >>> grouping = lst.groupingBy(lambda s: s[0])
            >>> result = grouping.each_count()
            >>> result.get('a')  # Returns 3
            >>> result.get('b')  # Returns 1
        """
        from kotcollections.kot_map import KotMap
        groups = self._group_by_key()
        counts = {key: len(values) for key, values in groups.items()}
        return KotMap(counts)

    def fold(
        self,
        initial_value_selector: Callable[[K, T], R],
        operation: Callable[[K, R, T], R]
    ) -> 'KotMap[K, R]':
        """Groups elements from the Grouping source by key and applies operation to each group sequentially,
        passing the previously accumulated value and the current element as arguments,
        and stores the results in a new map.

        An initial value of accumulator is provided by initialValueSelector function.

        Args:
            initial_value_selector: A function that provides an initial value for the accumulator
                                   for each group. Takes the key and the first element.
            operation: A function that is invoked on each element with the following parameters:
                      - key: the key of the group this element belongs to
                      - accumulator: the current value of the accumulator
                      - element: the element from the source being aggregated

        Returns:
            A KotMap associating the key of each group with the result of aggregation of the group elements.

        Examples:
            >>> lst = KotList([1, 2, 3, 4, 5, 6])
            >>> grouping = lst.groupingBy(lambda x: x % 2)
            >>> result = grouping.fold(
            ...     lambda k, e: 0,
            ...     lambda k, acc, e: acc + e
            ... )
            >>> result.get(0)  # Returns 12 (2+4+6)
            >>> result.get(1)  # Returns 9 (1+3+5)
        """
        from kotcollections.kot_map import KotMap
        groups = self._group_by_key()
        results = {}

        for key, elements in groups.items():
            if not elements:
                continue
            # Get initial value using first element
            accumulator = initial_value_selector(key, elements[0])
            # Fold over remaining elements
            for element in elements:
                accumulator = operation(key, accumulator, element)
            results[key] = accumulator

        return KotMap(results)

    def reduce(self, operation: Callable[[K, T, T], T]) -> 'KotMap[K, T]':
        """Groups elements from the Grouping source by key and applies the reducing operation
        to the elements of each group sequentially, starting from the second element of the group,
        passing the previously accumulated value and the current element as arguments,
        and stores the results in a new map.

        An initial value of accumulator is the first element of the group.

        Args:
            operation: A function that is invoked on each element (except the first)
                      with the following parameters:
                      - key: the key of the group this element belongs to
                      - accumulator: the current value of the accumulator
                      - element: the element from the source being aggregated

        Returns:
            A KotMap associating the key of each group with the result of aggregation of the group elements.

        Examples:
            >>> lst = KotList([1, 2, 3, 4, 5, 6])
            >>> grouping = lst.groupingBy(lambda x: x % 2)
            >>> result = grouping.reduce(lambda k, acc, e: acc + e)
            >>> result.get(0)  # Returns 12 (2+4+6)
            >>> result.get(1)  # Returns 9 (1+3+5)
        """
        from kotcollections.kot_map import KotMap
        groups = self._group_by_key()
        results = {}

        for key, elements in groups.items():
            if not elements:
                continue
            if len(elements) == 1:
                results[key] = elements[0]
            else:
                # Start with first element as accumulator
                accumulator = elements[0]
                # Reduce over remaining elements
                for element in elements[1:]:
                    accumulator = operation(key, accumulator, element)
                results[key] = accumulator

        return KotMap(results)

    def aggregate(
        self,
        operation: Callable[[K, Optional[R], T, bool], R]
    ) -> 'KotMap[K, R]':
        """Groups elements from the Grouping source by key and applies operation to the elements of each group
        sequentially, passing the previously accumulated value and the current element as arguments,
        and stores the results in a new map.

        An initial value of accumulator is null for each group.

        Args:
            operation: A function that is invoked on each element with the following parameters:
                      - key: the key of the group this element belongs to
                      - accumulator: the current value of the accumulator (None for first element)
                      - element: the element from the source being aggregated
                      - first: indicates whether it's the first element of the group

        Returns:
            A KotMap associating the key of each group with the result of aggregation of the group elements.

        Examples:
            >>> lst = KotList(["apple", "apricot", "banana"])
            >>> grouping = lst.groupingBy(lambda s: s[0])
            >>> result = grouping.aggregate(
            ...     lambda k, acc, e, first: e if first else acc + "," + e
            ... )
            >>> result.get('a')  # Returns "apple,apricot"
            >>> result.get('b')  # Returns "banana"
        """
        from kotcollections.kot_map import KotMap
        groups = self._group_by_key()
        results = {}

        for key, elements in groups.items():
            if not elements:
                continue

            accumulator: Optional[R] = None
            for i, element in enumerate(elements):
                is_first = (i == 0)
                accumulator = operation(key, accumulator, element, is_first)

            results[key] = accumulator

        return KotMap(results)

    def __repr__(self) -> str:
        return f"KotGrouping(source_size={len(self._source)})"
