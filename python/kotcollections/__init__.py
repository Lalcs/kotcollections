"""
kotcollections - A Python library that fully reproduces Kotlin's Collections interfaces.

This library is implemented in Rust using PyO3 for maximum performance.
"""

from kotcollections._kotcollections import (
    KotList,
    KotMutableList,
    KotSet,
    KotMutableSet,
    KotMap,
    KotMutableMap,
    KotGrouping,
)

__all__ = [
    "KotList",
    "KotMutableList",
    "KotSet",
    "KotMutableSet",
    "KotMap",
    "KotMutableMap",
    "KotGrouping",
]
