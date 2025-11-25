# Interfaces (ABC)
from .interfaces import (
    IKotIterable,
    IKotCollection,
    IKotList,
    IKotSet,
    IKotMap,
    IKotMutableIterable,
    IKotMutableCollection,
    IKotMutableList,
    IKotMutableSet,
    IKotMutableMap,
)

# Extension Interfaces (ABC)
from .extensions import (
    IKotIterableExtensions,
    IKotListExtensions,
    IKotMapExtensions,
)

# Implementations
from .kot_grouping import KotGrouping
from .kot_list import KotList
from .kot_map import KotMap, KotMapWithDefault
from .kot_mutable_list import KotMutableList
from .kot_mutable_map import KotMutableMap
from .kot_mutable_set import KotMutableSet
from .kot_set import KotSet

__all__ = [
    # Interfaces
    'IKotIterable',
    'IKotCollection',
    'IKotList',
    'IKotSet',
    'IKotMap',
    'IKotMutableIterable',
    'IKotMutableCollection',
    'IKotMutableList',
    'IKotMutableSet',
    'IKotMutableMap',
    # Extension Interfaces
    'IKotIterableExtensions',
    'IKotListExtensions',
    'IKotMapExtensions',
    # Implementations
    'KotList',
    'KotMutableList',
    'KotSet',
    'KotMutableSet',
    'KotMap',
    'KotMutableMap',
    'KotMapWithDefault',
    'KotGrouping',
]

# Version will be dynamically set by poetry-dynamic-versioning
try:
    from ._version import __version__
except ImportError:
    # Fallback for development
    __version__ = '0.0.0'
