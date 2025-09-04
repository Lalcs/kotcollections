# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Conversation Guidelines

- **Always speak in Japanese**

## Development Philosophy

- Focus on clean, maintainable code
- Follow these design principles
    - SOLID principles
        - **Single Responsibility**: Each class, function, or module has one reason to change
        - **Open/Closed**: Software entities should be open for extension but closed for modification
        - **Liskov Substitution**: Derived classes must be substitutable for their base classes
        - **Interface Segregation**: Clients should not be forced to depend on interfaces they don't use
        - **Dependency Inversion**: Depend on abstractions, not concretions
    - Core Design Principles
        - **DRY**: Abstract common functionality, eliminate duplication
        - **KISS**: Prefer simplicity over complexity in all design decisions
        - **YAGNI**: Implement only current requirements, avoid speculative features
        - **Composition Over Inheritance**: Favor object composition over class inheritance
        - **Separation of Concerns**: Divide program functionality into distinct sections
        - **Loose Coupling**: Minimize dependencies between components
        - **High Cohesion**: Related functionality should be grouped together logically

## Web Operations via Sub-Agents

**Always use sub-agents for WebFetch and WebSearch operations to prevent context overflow.**

### Implementation Guidelines

When performing web operations:

1. **Delegate to Sub-Agents**
    - Never execute WebFetch or WebSearch directly in the main context
    - Create a sub-agent specifically for web operations

2. **Sub-Agent Instructions**
    - The sub-agent should receive clear, specific search/fetch tasks
    - It must summarize findings into concise, relevant information
    - Return only essential data points, not raw search results

## Kotlin Documentation Research

**Always use context7 when researching Kotlin documentation.**

### Guidelines

When users ask about Kotlin language features, standard library, or API:

1. **Use context7 MCP server**
    - First use `mcp__context7__resolve-library-id` to find the appropriate Kotlin library
    - Then use `mcp__context7__get-library-docs` to retrieve detailed documentation

2. **Library Selection**
    - For general Kotlin documentation: `/jetbrains/kotlin-web-site`
    - For language core: `/jetbrains/kotlin`
    - For coroutines: `/kotlin/kotlinx.coroutines`
    - For serialization: `/kotlin/kotlinx.serialization`

## Project Overview

**kotcollections** is a Python library that provides a complete implementation of Kotlin's collection interfaces for
Python
developers. It offers Kotlin's rich collection operations (List, Map, Set) with Python's snake_case naming convention,
full type safety, and 100% test coverage.

## Development Environment Setup

### Prerequisites

- Python 3.13 or higher
- Poetry (for dependency management)

### Virtual Environment

The project is configured to create virtual environments within the project directory (`.venv/`).

## Essential Commands

### Environment Setup

```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell

# Add a new dependency
poetry add <package_name>

# Add a development dependency
poetry add --group dev <package_name>
```

### Testing

```bash
# Run tests with unittest
python -m unittest discover -v

# Run tests with coverage
python -m coverage run -m unittest discover
python -m coverage report -m

# Run a specific test file
python -m unittest tests.test_kot_list -v

# Run a specific test
python -m unittest tests.test_kot_list.TestKotListBasics.test_init_empty

# Run tests for a specific feature
python -m unittest discover -v -k "TypeSpecification"
```

### Code Quality

```bash
# Run linters (once configured)
poetry run ruff check .
poetry run ruff format .

# Type checking (once configured)
poetry run mypy kotcollections
```

### Building and Distribution

```bash
# Build the project
poetry build

# Show project information
poetry show

# Update dependencies
poetry update
```

## Project Structure

```
kotcollections/
├── kotcollections/              # Main package directory
│   ├── __init__.py             # Package initialization (exports all collection classes)
│   ├── kot_list.py             # Read-only KotList implementation
│   ├── kot_mutable_list.py     # Mutable KotMutableList implementation
│   ├── kot_map.py              # Read-only KotMap implementation
│   ├── kot_mutable_map.py      # Mutable KotMutableMap implementation
│   ├── kot_set.py              # Read-only KotSet implementation
│   └── kot_mutable_set.py      # Mutable KotMutableSet implementation
├── tests/                       # Test directory
│   ├── __init__.py             # Test package initialization
│   ├── test_circular_imports.py # Tests for circular import issues
│   ├── test_kot_list.py        # Tests for KotList (100% coverage)
│   ├── test_kot_mutable_list.py # Tests for KotMutableList (100% coverage)
│   ├── test_kot_map.py         # Tests for KotMap (100% coverage)
│   ├── test_kot_mutable_map.py  # Tests for KotMutableMap (100% coverage)
│   ├── test_kot_set.py         # Tests for KotSet (100% coverage)
│   └── test_kot_mutable_set.py  # Tests for KotMutableSet (100% coverage)
├── README.md           # Comprehensive documentation in English
├── pyproject.toml      # Poetry and project configuration
├── poetry.toml         # Poetry-specific configuration (virtual env in project)
└── poetry.lock         # Locked dependencies (auto-generated)
```

## Architecture Notes

### Core Design

1. **KotList**: Read-only list implementation with all Kotlin List methods
    - Immutable after creation
    - Type-safe with runtime type checking
    - Supports method chaining

2. **KotMutableList**: Extends KotList with mutation methods
    - All KotList methods plus add, remove, sort, etc.
    - Maintains type safety during modifications
    - Supports in-place operations

3. **KotMap**: Read-only map implementation with all Kotlin Map methods
    - Immutable after creation
    - Type-safe key-value pairs
    - Rich transformation and filtering operations

4. **KotMutableMap**: Extends KotMap with mutation methods
    - All KotMap methods plus put, remove, clear, etc.
    - Maintains type safety for keys and values
    - Advanced operations like compute, merge, replace

5. **KotSet**: Read-only set implementation with all Kotlin Set methods
    - Immutable after creation
    - Type-safe unique elements
    - Set operations like union, intersection, difference

6. **KotMutableSet**: Extends KotSet with mutation methods
    - All KotSet methods plus add, remove, clear, etc.
    - Maintains type safety during modifications
    - Bulk operations like add_all, remove_all, retain_all

### Type Safety

1. **Runtime Type Checking**: Ensures single element type per collection
    - First element determines the collection's type by default
    - Type errors are raised immediately on invalid operations
    - Collections can be nested (like `List<List<T>>` in Kotlin)

2. **Explicit Type Specification** (Added 2025-07-24):
    - `__class_getitem__` syntax: `KotList[Animal]()` creates an Animal-typed list
    - `of_type` class method: `KotList.of_type(Animal, elements)` with explicit type
    - Solves the interface type initialization problem
    - Allows parent type collections to accept subclass instances

3. **Type Preservation**: Type information is maintained during conversions
    - `to_kot_list()`, `to_kot_mutable_list()` preserve element types
    - `to_kot_set()`, `to_kot_mutable_set()` preserve element types
    - `to_kot_map()`, `to_kot_mutable_map()` preserve key and value types

### Pythonic Naming Aliases

To provide a more Pythonic API, all methods ending with `_null` have corresponding `_none` aliases:

- `get_or_null()` → `get_or_none()`
- `first_or_null()` → `first_or_none()`
- `first_or_null_predicate()` → `first_or_none_predicate()`
- `last_or_null()` → `last_or_none()`
- `last_or_null_predicate()` → `last_or_none_predicate()`
- `element_at_or_null()` → `element_at_or_none()`
- `map_not_null()` → `map_not_none()`
- `filter_not_null()` → `filter_not_none()`
- `max_or_null()` → `max_or_none()`
- `min_or_null()` → `min_or_none()`
- `max_by_or_null()` → `max_by_or_none()`
- `min_by_or_null()` → `min_by_or_none()`

Both naming styles are fully supported and can be used interchangeably based on preference.

### Key Features

- Complete Kotlin collection API compatibility (List, Map, Set)
- Snake_case naming convention (e.g., `first_or_null()` instead of `firstOrNull()`)
- Pythonic `_none` aliases for all `_null` methods (e.g., `first_or_none()` as an alias for `first_or_null()`)
- Explicit type specification with `KotList[Type]()` syntax and `of_type()` method
- Type preservation across all collection conversions
- Rich functional operations: map, filter, fold, reduce, etc.
- Comprehensive aggregation: sum_of, average, max_by_or_null, etc.
- Advanced grouping: group_by, chunked, windowed
- Set operations: union, intersection, difference, symmetric_difference
- Map operations: filter_keys, filter_values, map_keys, map_values
- 100% test coverage with unittest

## Development Workflow

1. Always work within the Poetry virtual environment
2. Before committing, ensure all tests pass with `python -m unittest discover`
3. Verify 100% test coverage with `python -m coverage run -m unittest discover && python -m coverage report`
4. Keep dependencies minimal and well-documented in `pyproject.toml`
5. Use type hints for better code clarity and IDE support
6. Follow the established patterns in kot_list.py when adding new methods

## Configuration

The project uses Poetry's `pyproject.toml` for all project configuration. Key settings:

- Python version requirement: >=3.13
- Virtual environments are created in-project (see `poetry.toml`)

## Development History

### 2025-07-19: Pythonic `_none` Aliases

- Added `_none` aliases for all methods ending with `_null` to provide a more Pythonic API
- Total of 12 alias methods added across access, transformation, filtering, and aggregation operations
- All aliases are simple delegations to the original `_null` methods
- Added comprehensive tests for all alias methods, maintaining 100% code coverage
- Both naming conventions (`_null` and `_none`) are now fully supported

### 2025-07-24: Type Specification and Type Preservation

- **Added explicit type specification features**:
    - `__class_getitem__` syntax: `KotList[Animal]()` for creating typed collections
    - `of_type` class method: `KotList.of_type(Animal, elements)` for explicit typing
    - Implemented for all collection types: List, Map, Set (both mutable and immutable)
    - Solves the interface type initialization problem where parent type collections can accept subclass instances

- **Improved type preservation**:
    - All conversion methods (`to_kot_list()`, `to_kot_mutable_list()`, etc.) now preserve type information
    - Type safety is maintained across collection transformations
    - Added comprehensive tests for type preservation

- **Type checking improvements**:
    - Fixed inconsistency where KotList used strict type checking while Map/Set used isinstance()
    - All collections now use isinstance() for consistent polymorphic behavior
    - Added inheritance-based type checking tests for all collection types