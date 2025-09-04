# Kotlin Collection API Reference

## Collection Interface (共通)
- `size: Int` ✅
- `isEmpty(): Boolean` ✅
- `contains(element: E): Boolean` ✅ 
- `iterator(): Iterator<E>` ✅
- `containsAll(elements: Collection<E>): Boolean` ✅

## Iterable Interface
- `forEach(action: (T) -> Unit): Unit` ✅
- `onEach(action: (T) -> Unit): Iterable<T>` ✅

## List Interface
### Basic Operations
- `get(index: Int): E` ✅
- `indexOf(element: E): Int` ✅
- `lastIndexOf(element: E): Int` ✅
- `listIterator(): ListIterator<E>` ✅ (simplified)
- `listIterator(index: Int): ListIterator<E>` ✅ (simplified)
- `subList(fromIndex: Int, toIndex: Int): List<E>` ✅

### Extension Functions
- `first(): T` ✅
- `first(predicate: (T) -> Boolean): T` ✅
- `firstOrNull(): T?` ✅
- `firstOrNull(predicate: (T) -> Boolean): T?` ✅
- `last(): T` ✅
- `last(predicate: (T) -> Boolean): T` ✅
- `lastOrNull(): T?` ✅
- `lastOrNull(predicate: (T) -> Boolean): T?` ✅
- `getOrElse(index: Int, defaultValue: (Int) -> T): T` ✅
- `getOrNull(index: Int): T?` ✅
- `elementAt(index: Int): T` ✅
- `elementAtOrElse(index: Int, defaultValue: (Int) -> T): T` ✅
- `elementAtOrNull(index: Int): T?` ✅

### Transformation
- `map(transform: (T) -> R): List<R>` ✅
- `mapIndexed(transform: (index: Int, T) -> R): List<R>` ✅
- `mapNotNull(transform: (T) -> R?): List<R>` ✅
- `mapIndexedNotNull(transform: (index: Int, T) -> R?): List<R>` ✅
- `flatMap(transform: (T) -> Iterable<R>): List<R>` ✅
- `flatMapIndexed(transform: (index: Int, T) -> Iterable<R>): List<R>` ✅
- `flatten(): List<T>` ✅

### Filtering
- `filter(predicate: (T) -> Boolean): List<T>` ✅
- `filterIndexed(predicate: (index: Int, T) -> Boolean): List<T>` ✅
- `filterNot(predicate: (T) -> Boolean): List<T>` ✅
- `filterNotNull(): List<T>` ✅
- `filterIsInstance<R>(): List<R>` ✅

### Predicates
- `all(predicate: (T) -> Boolean): Boolean` ✅
- `any(): Boolean` ✅
- `any(predicate: (T) -> Boolean): Boolean` ✅
- `none(predicate: (T) -> Boolean): Boolean` ✅
- `count(): Int` ✅
- `count(predicate: (T) -> Boolean): Int` ✅

### Aggregation
- `fold(initial: R, operation: (acc: R, T) -> R): R` ✅
- `foldIndexed(initial: R, operation: (index: Int, acc: R, T) -> R): R` ✅
- `foldRight(initial: R, operation: (T, acc: R) -> R): R` ✅
- `foldRightIndexed(initial: R, operation: (index: Int, T, acc: R) -> R): R` ✅
- `reduce(operation: (acc: T, T) -> T): T` ✅
- `reduceIndexed(operation: (index: Int, acc: T, T) -> T): T` ✅
- `reduceRight(operation: (T, acc: T) -> T): T` ✅
- `reduceRightIndexed(operation: (index: Int, T, acc: T) -> T): T` ✅
- `reduceOrNull(operation: (acc: T, T) -> T): T?` ✅
- `sum(): T` ❌ (primitive types only in Kotlin)
- `sumOf(selector: (T) -> R): R` ✅
- `average(): Double` ❌ (primitive types only in Kotlin) 
- `maxOrNull(): T?` ✅
- `minOrNull(): T?` ✅
- `maxByOrNull(selector: (T) -> R): T?` ✅
- `minByOrNull(selector: (T) -> R): T?` ✅
- `maxOfOrNull(selector: (T) -> R): R?` ✅
- `minOfOrNull(selector: (T) -> R): R?` ✅

### Grouping
- `groupBy(keySelector: (T) -> K): Map<K, List<T>>` ✅
- `groupBy(keySelector: (T) -> K, valueTransform: (T) -> V): Map<K, List<V>>` ✅
- `chunked(size: Int): List<List<T>>` ✅
- `chunked(size: Int, transform: (List<T>) -> R): List<R>` ✅
- `windowed(size: Int): List<List<T>>` ✅
- `windowed(size: Int, step: Int): List<List<T>>` ✅
- `windowed(size: Int, step: Int, partialWindows: Boolean): List<List<T>>` ✅

### Sorting
- `sorted(): List<T>` ✅
- `sortedBy(selector: (T) -> R): List<T>` ✅
- `sortedByDescending(selector: (T) -> R): List<T>` ✅
- `sortedDescending(): List<T>` ✅
- `sortedWith(comparator: Comparator<in T>): List<T>` ✅

### Set Operations
- `distinct(): List<T>` ✅
- `distinctBy(selector: (T) -> K): List<T>` ✅
- `intersect(other: Iterable<T>): List<T>` ✅
- `subtract(other: Iterable<T>): List<T>` ❌
- `union(other: Iterable<T>): List<T>` ✅

### Collection Operations
- `plus(element: T): List<T>` ✅
- `plus(elements: Iterable<T>): List<T>` ✅
- `minus(element: T): List<T>` ✅
- `minus(elements: Iterable<T>): List<T>` ✅

### Slicing
- `take(n: Int): List<T>` ✅
- `takeLast(n: Int): List<T>` ✅
- `takeWhile(predicate: (T) -> Boolean): List<T>` ✅
- `takeLastWhile(predicate: (T) -> Boolean): List<T>` ✅
- `drop(n: Int): List<T>` ✅
- `dropLast(n: Int): List<T>` ✅
- `dropWhile(predicate: (T) -> Boolean): List<T>` ✅
- `dropLastWhile(predicate: (T) -> Boolean): List<T>` ✅
- `slice(indices: IntRange): List<T>` ❌
- `slice(indices: Iterable<Int>): List<T>` ✅

### Search
- `binarySearch(element: T): Int` ✅
- `binarySearch(element: T, comparator: Comparator<in T>): Int` ✅
- `binarySearchBy(selector: (T) -> K, key: K): Int` ✅
- `find(predicate: (T) -> Boolean): T?` ✅
- `findLast(predicate: (T) -> Boolean): T?` ✅
- `indexOfFirst(predicate: (T) -> Boolean): Int` ✅
- `indexOfLast(predicate: (T) -> Boolean): Int` ✅

### Random
- `random(): T` ✅
- `randomOrNull(): T?` ✅
- `shuffled(): List<T>` ✅

### Zipping
- `zip(other: Iterable<R>): List<Pair<T, R>>` ✅
- `zip(other: Iterable<R>, transform: (a: T, b: R) -> V): List<V>` ✅
- `zipWithNext(): List<Pair<T, T>>` ✅
- `zipWithNext(transform: (a: T, b: T) -> R): List<R>` ✅
- `unzip(): Pair<List<T>, List<R>>` ✅

### Misc
- `reversed(): List<T>` ✅
- `asReversed(): List<T>` ✅
- `asSequence(): Sequence<T>` ✅
- `joinToString(): String` ✅
- `partition(predicate: (T) -> Boolean): Pair<List<T>, List<T>>` ✅

## MutableList Interface
### Mutation
- `add(element: E): Boolean` ✅
- `add(index: Int, element: E): Unit` ✅
- `addAll(elements: Collection<E>): Boolean` ✅
- `addAll(index: Int, elements: Collection<E>): Boolean` ✅
- `remove(element: E): Boolean` ✅
- `removeAt(index: Int): E` ✅
- `removeAll(elements: Collection<E>): Boolean` ✅
- `retainAll(elements: Collection<E>): Boolean` ✅
- `clear(): Unit` ✅
- `set(index: Int, element: E): E` ✅

### Additional Mutable Operations
- `removeFirst(): E` ❌
- `removeFirstOrNull(): E?` ❌ 
- `removeLast(): E` ❌
- `removeLastOrNull(): E?` ❌
- `removeIf(filter: (T) -> Boolean): Boolean` ❌
- `replaceAll(operator: (T) -> T): Unit` ❌
- `fill(value: T): Unit` ✅
- `shuffle(): Unit` ✅
- `reverse(): Unit` ✅
- `sort(): Unit` ✅
- `sortBy(selector: (T) -> R): Unit` ✅
- `sortByDescending(selector: (T) -> R): Unit` ✅
- `sortWith(comparator: Comparator<in T>): Unit` ✅
- `sortDescending(): Unit` ✅

## Set Interface
### Basic Operations
- `contains(element: E): Boolean` ✅
- `containsAll(elements: Collection<E>): Boolean` ✅
- `isEmpty(): Boolean` ✅
- `size: Int` ✅

### Extension Functions (similar to List but with Set semantics)
- Most of the List extension functions apply to Set as well ✅

### Set-specific Operations  
- `intersect(other: Iterable<T>): Set<T>` ✅
- `union(other: Iterable<T>): Set<T>` ✅
- `subtract(other: Iterable<T>): Set<T>` ✅
- `plus(element: T): Set<T>` ✅
- `plus(elements: Iterable<T>): Set<T>` ✅
- `minus(element: T): Set<T>` ✅
- `minus(elements: Iterable<T>): Set<T>` ✅

## MutableSet Interface
### Mutation
- `add(element: E): Boolean` ✅
- `addAll(elements: Collection<E>): Boolean` ✅
- `remove(element: E): Boolean` ✅
- `removeAll(elements: Collection<E>): Boolean` ✅
- `retainAll(elements: Collection<E>): Boolean` ✅
- `clear(): Unit` ✅

### Additional Mutable Operations
- `removeIf(filter: (T) -> Boolean): Boolean` ✅
- Operator overloads (`+=`, `-=`, etc.) ✅

## Map Interface
### Basic Operations
- `get(key: K): V?` ✅
- `containsKey(key: K): Boolean` ✅
- `containsValue(value: V): Boolean` ✅
- `isEmpty(): Boolean` ✅
- `size: Int` ✅
- `keys: Set<K>` ✅
- `values: Collection<V>` ✅
- `entries: Set<Map.Entry<K, V>>` ✅

### Extension Functions
- `getValue(key: K): V` ✅
- `getOrDefault(key: K, defaultValue: V): V` ✅
- `getOrElse(key: K, defaultValue: () -> V): V` ✅
- `getOrPut(key: K, defaultValue: () -> V): V` ❌ (MutableMap only)
- `getValue(key: K): V` ✅

### Transformation
- `map(transform: (Map.Entry<K, V>) -> R): List<R>` ✅
- `mapKeys(transform: (Map.Entry<K, V>) -> R): Map<R, V>` ✅
- `mapValues(transform: (Map.Entry<K, V>) -> R): Map<K, R>` ✅
- `mapNotNull(transform: (Map.Entry<K, V>) -> R?): List<R>` ✅

### Filtering
- `filter(predicate: (Map.Entry<K, V>) -> Boolean): Map<K, V>` ✅
- `filterKeys(predicate: (K) -> Boolean): Map<K, V>` ✅  
- `filterValues(predicate: (V) -> Boolean): Map<K, V>` ✅
- `filterNot(predicate: (Map.Entry<K, V>) -> Boolean): Map<K, V>` ✅
- `filterNotNull(): Map<K, V>` ✅

### Collection Operations
- `plus(pair: Pair<K, V>): Map<K, V>` ✅
- `plus(pairs: Iterable<Pair<K, V>>): Map<K, V>` ✅
- `plus(map: Map<K, V>): Map<K, V>` ✅
- `minus(key: K): Map<K, V>` ✅
- `minus(keys: Iterable<K>): Map<K, V>` ✅

### Other Map Operations
- `forEach(action: (Map.Entry<K, V>) -> Unit): Unit` ✅
- `all(predicate: (Map.Entry<K, V>) -> Boolean): Boolean` ✅
- `any(predicate: (Map.Entry<K, V>) -> Boolean): Boolean` ✅
- `none(predicate: (Map.Entry<K, V>) -> Boolean): Boolean` ✅
- `count(predicate: (Map.Entry<K, V>) -> Boolean): Int` ✅
- `maxByOrNull(selector: (Map.Entry<K, V>) -> R): Map.Entry<K, V>?` ✅
- `minByOrNull(selector: (Map.Entry<K, V>) -> R): Map.Entry<K, V>?` ✅
- `toList(): List<Pair<K, V>>` ✅

## MutableMap Interface  
### Mutation
- `put(key: K, value: V): V?` ✅
- `putAll(from: Map<out K, V>): Unit` ✅
- `remove(key: K): V?` ✅
- `remove(key: K, value: V): Boolean` ✅
- `clear(): Unit` ✅

### Additional Mutable Operations
- `getOrPut(key: K, defaultValue: () -> V): V` ✅
- `putIfAbsent(key: K, value: V): V?` ✅
- `replace(key: K, value: V): V?` ✅
- `replace(key: K, oldValue: V, newValue: V): Boolean` ✅
- `replaceAll(function: (K, V) -> V): Unit` ✅
- `compute(key: K, remappingFunction: (K, V?) -> V?): V?` ✅
- `computeIfAbsent(key: K, mappingFunction: (K) -> V): V` ✅
- `computeIfPresent(key: K, remappingFunction: (K, V) -> V?): V?` ✅
- `merge(key: K, value: V, remappingFunction: (V, V) -> V?): V?` ✅
- Operator overloads (`+=`, `-=`, etc.) ✅

## 不足している重要なAPI

### List関連
1. `subtract(other: Iterable<T>): List<T>` - Set差集合のList版
2. `slice(indices: IntRange): List<T>` - 範囲指定のslice  
3. `removeFirst(): E`, `removeFirstOrNull(): E?` (MutableList)
4. `removeLast(): E`, `removeLastOrNull(): E?` (MutableList)
5. `removeIf(filter: (T) -> Boolean): Boolean` (MutableList)
6. `replaceAll(operator: (T) -> T): Unit` (MutableList)

### 型別名・定数
7. `indices: IntRange` property (現在のindicesプロパティとは異なる)

### プリミティブ特化API
8. `sum(): T` - 数値型専用
9. `average(): Double` - 数値型専用

これらのうち、特に重要なのは:
1. `subtract()` - Set演算の完全性のため
2. `slice(IntRange)` - よく使われる操作
3. MutableListの`removeFirst/Last()`系 - 便利なAPI
4. `removeIf()` - 条件による削除
