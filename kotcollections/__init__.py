# Interfaces (ABC)
from .interfaces import (
    KotlinIterable,
    KotlinCollection,
    KotlinList,
    KotlinSet,
    KotlinMap,
    KotlinMutableIterable,
    KotlinMutableCollection,
    KotlinMutableList,
    KotlinMutableSet,
    KotlinMutableMap,
    # Factory Mixin
    KotlinCollectionFactory,
    KotlinMapFactory,
    # Pythonic Alias Mixin
    PythonicListAliases,
)

# Extension Interfaces (ABC)
from .extensions import (
    KotlinIterableExtensions,
    KotlinListExtensions,
    KotlinMapExtensions,
    # Pythonic Alias Mixin
    PythonicIterableExtensionAliases,
    PythonicListExtensionAliases,
    PythonicMutableListAliases,
    PythonicMapExtensionAliases,
    PythonicSetAliases,
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
    'KotlinIterable',
    'KotlinCollection',
    'KotlinList',
    'KotlinSet',
    'KotlinMap',
    'KotlinMutableIterable',
    'KotlinMutableCollection',
    'KotlinMutableList',
    'KotlinMutableSet',
    'KotlinMutableMap',
    # Factory Mixin Interfaces
    'KotlinCollectionFactory',
    'KotlinMapFactory',
    # Extension Interfaces
    'KotlinIterableExtensions',
    'KotlinListExtensions',
    'KotlinMapExtensions',
    # Pythonic Alias Mixin Interfaces
    'PythonicListAliases',
    'PythonicIterableExtensionAliases',
    'PythonicListExtensionAliases',
    'PythonicMutableListAliases',
    'PythonicMapExtensionAliases',
    'PythonicSetAliases',
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
