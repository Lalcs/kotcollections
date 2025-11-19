"""
TypeChecker: Utility class for runtime type checking in collections.

This module provides shared type checking logic used across KotList, KotMap,
KotSet and their mutable variations.
"""

from typing import Any, Optional, Type


class TypeChecker:
    """Utility class for runtime type checking in collections."""

    @staticmethod
    def is_valid_element_type(element: Any, expected_type: Optional[Type]) -> bool:
        """Check if an element matches the expected type.

        Args:
            element: The element to check
            expected_type: The expected type, or None if no type constraint

        Returns:
            True if the element matches the expected type or if no type is set

        Type Checking Rules:
            - If expected_type is None, returns True (no constraint)
            - If expected_type is not a real type, returns True (skip checking)
            - Direct type match: element is instance of expected_type
            - Subclass match: element is instance of subclass of expected_type
            - Collection type match: special handling for Kot* collection types
            - __class_getitem__ type match: types created via KotList[T] syntax
        """
        # No type constraint set
        if expected_type is None:
            return True

        # Skip checking if expected_type is not a real type (e.g., TypeVar)
        if not isinstance(expected_type, type):
            return True

        # Direct instance check
        if isinstance(element, expected_type):
            return True

        # Special handling for __class_getitem__ types (e.g., KotList[Task])
        if TypeChecker._is_class_getitem_type_match(element, expected_type):
            return True

        return False

    @staticmethod
    def _is_class_getitem_type_match(element: Any, expected_type: Type) -> bool:
        """Check if element matches a __class_getitem__ generated type.

        This handles cases where expected_type was created via syntax like
        KotList[Animal], KotMap[str, int], etc.

        Args:
            element: The element to check
            expected_type: The expected type (potentially from __class_getitem__)

        Returns:
            True if element matches the __class_getitem__ generated type
        """
        # Check if this looks like a __class_getitem__ generated type
        if not (hasattr(expected_type, '__base__') and
                hasattr(expected_type, '__name__')):
            return False

        # More reliable check: see if the type name starts with the base class name
        # and contains '[', indicating it's a parameterized type
        base_class_name = getattr(expected_type.__base__, '__name__', '')
        if not base_class_name:
            return False

        type_name = expected_type.__name__
        # Check if it's a parameterized type like "KotList[Animal]"
        if not (type_name.startswith(base_class_name + '[') and ']' in type_name):
            return False

        # Element should be an instance of the base class
        return isinstance(element, expected_type.__base__)

    @staticmethod
    def validate_element(element: Any, expected_type: Optional[Type],
                        collection_name: str) -> None:
        """Validate an element's type and raise TypeError if invalid.

        Args:
            element: The element to validate
            expected_type: The expected type
            collection_name: Name of the collection for error messages

        Raises:
            TypeError: If the element doesn't match the expected type
        """
        if not TypeChecker.is_valid_element_type(element, expected_type):
            expected_name = getattr(expected_type, '__name__', str(expected_type))
            element_type_name = type(element).__name__
            raise TypeError(
                f"Cannot add element of type '{element_type_name}' "
                f"to {collection_name}[{expected_name}]"
            )

    @staticmethod
    def should_skip_type_checking(expected_type: Optional[Type]) -> bool:
        """Check if type checking should be skipped.

        Args:
            expected_type: The expected type to check

        Returns:
            True if type checking should be skipped
        """
        # Skip if no type is set
        if expected_type is None:
            return True

        # Skip if it's not a real type (e.g., TypeVar)
        if not isinstance(expected_type, type):
            return True

        return False

    @staticmethod
    def infer_element_type(element: Any, collection_base_class: Type) -> Type:
        """Infer the type of an element, with special handling for collections.

        Args:
            element: The element whose type to infer
            collection_base_class: The base collection class (e.g., KotList)

        Returns:
            The inferred type of the element
        """
        # Special handling for Kot* collection types
        if isinstance(element, collection_base_class):
            return collection_base_class

        return type(element)
