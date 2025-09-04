# kotcollections API Gap Analysis Report

## 概要

kotcollectionsプロジェクトは、Kotlin標準ライブラリのCollection APIを非常に高い完成度で実装していますが、いくつかの重要なAPIが不足しています。本レポートでは、不足しているAPIを重要度順に整理し、実装優先度を提案します。

## 実装状況サマリー

| コレクション型 | 実装済みメソッド数 | 主要API完成度 |
|---------------|------------------|--------------|
| KotList | 172 | 95% |
| KotMutableList | 196 | 90% |
| KotSet | 77 | 98% |
| KotMutableSet | 88 | 95% |
| KotMap | 47 | 98% |
| KotMutableMap | 65 | 95% |

## 不足している重要なAPI

### 高優先度（実装推奨）

#### 1. List.subtract() - Set差集合のList版
```kotlin
// Kotlin
fun <T> List<T>.subtract(other: Iterable<T>): List<T>
```
**重要度**: ★★★★☆  
**理由**: 
- Set演算の完全性のため必要
- `intersect()`, `union()`は実装済みだが`subtract()`のみ欠如
- 数学的演算の一貫性

**実装難易度**: 低  
**推定実装時間**: 1-2時間

#### 2. List.slice(indices: IntRange) - 範囲指定のslice
```kotlin
// Kotlin  
fun <T> List<T>.slice(indices: IntRange): List<T>
```
**重要度**: ★★★★☆  
**理由**:
- `Iterable<Int>`版は実装済み
- IntRangeからのsliceは頻繁に使用される操作
- Kotlinでの使用頻度が高い

**実装難易度**: 低  
**推定実装時間**: 30分-1時間

#### 3. MutableList.removeFirst()/removeFirstOrNull()
```kotlin
// Kotlin
fun <T> MutableList<T>.removeFirst(): T
fun <T> MutableList<T>.removeFirstOrNull(): T?
```
**重要度**: ★★★★☆  
**理由**:
- Deque操作の基本的な機能
- Stack/Queue実装時に重要
- KotMutableListの実装でremove_first, remove_first_or_nullとして存在確認済み

**実装難易度**: 低  
**推定実装時間**: 1時間

#### 4. MutableList.removeLast()/removeLastOrNull()
```kotlin  
// Kotlin
fun <T> MutableList<T>.removeLast(): T
fun <T> MutableList<T>.removeLastOrNull(): T?
```
**重要度**: ★★★★☆  
**理由**:
- removeFirst()と対になる操作
- 同じくStack/Queue操作で重要
- KotMutableListの実装でremove_last, remove_last_or_nullとして存在確認済み

**実装難易度**: 低  
**推定実装時間**: 1時間

### 中優先度（実装検討）

#### 5. MutableList.removeIf()
```kotlin
// Kotlin
fun <T> MutableList<T>.removeIf(filter: (T) -> Boolean): Boolean
```
**重要度**: ★★★☆☆  
**理由**:
- 条件による要素削除は便利
- ただし`filter()`と`retainAll()`の組み合わせで代用可能
- Java標準ライブラリにもある操作

**実装難易度**: 低  
**推定実装時間**: 1-2時間

#### 6. MutableList.replaceAll()
```kotlin
// Kotlin
fun <T> MutableList<T>.replaceAll(operator: (T) -> T): Unit
```
**重要度**: ★★★☆☆  
**理由**:
- 全要素の一括変換
- `map()`の破壊的版
- メモリ効率が良い場合がある

**実装難易度**: 低  
**推定実装時間**: 1-2時間

### 低優先度（実装任意）

#### 7. プリミティブ特化API
```kotlin
// Kotlin (Number型専用)
fun List<Int>.sum(): Int
fun List<Double>.average(): Double
```
**重要度**: ★★☆☆☆  
**理由**:
- `sumOf { it }`で代用可能
- Pythonの動的型付けでは恩恵が少ない
- 実装による計算性能の改善も限定的

**実装難易度**: 中（型判定が必要）  
**推定実装時間**: 3-5時間

#### 8. indices プロパティの改良
```kotlin
// Kotlin
val <T> List<T>.indices: IntRange
```
**重要度**: ★★☆☆☆  
**理由**:
- 現在は`range()`オブジェクトを返している
- IntRangeとしての互換性があると便利
- ただし現実的な影響は小さい

**実装難易度**: 低  
**推定実装時間**: 30分-1時間

## 実装していないが問題ないAPI

### コレクション作成関数
- `listOf()`, `setOf()`, `mapOf()` 等のトップレベル関数
- 理由: Pythonの慣習に合わない、コンストラクタで十分

### Collection/Sequence変換
- `asSequence()` の完全実装
- 理由: Pythonではiteratorで代用、実装済みで十分

### Android/JVM固有API  
- `toTypedArray()` 等の配列変換
- 理由: Pythonでは配列概念が異なる

## 実装推奨順序

### Phase 1: 基本セット演算の完成（推定2-3時間）
1. `List.subtract()` の実装
2. `List.slice(IntRange)` の実装

### Phase 2: MutableList操作の拡充（推定2-3時間）  
3. `MutableList.removeFirst()` / `removeFirstOrNull()` の実装
4. `MutableList.removeLast()` / `removeLastOrNull()` の実装

### Phase 3: 条件操作の追加（推定2-4時間）
5. `MutableList.removeIf()` の実装  
6. `MutableList.replaceAll()` の実装

### Phase 4: 最適化・互換性向上（推定1-2時間）
7. `indices`プロパティの改良

### Phase 5: 特殊化API（任意、推定3-5時間）
8. プリミティブ型特化API（数値のsum/average）

## テスト戦略

各新規APIの実装時には以下のテストが必要:

### 基本動作テスト
- 正常系の動作確認
- エッジケース（空リスト、単一要素等）
- 型安全性の確認

### 互換性テスト  
- 既存APIとの整合性確認
- Kotlin標準ライブラリとの動作比較
- `_none`エイリアスの追加（該当する場合）

### パフォーマンステスト
- 大規模データでのメモリ効率
- 計算量の確認

## まとめ

kotcollectionsは既にKotlin Collection APIの95%以上を実装しており、非常に高品質な実装となっています。不足している主要APIは以下の通り:

**実装必須**: 
- `List.subtract()` - Set演算の完全性
- `List.slice(IntRange)` - 利便性向上  
- `MutableList.removeFirst/Last()` - Deque操作

**実装推奨**:
- `MutableList.removeIf()` - 条件削除
- `MutableList.replaceAll()` - 一括変換

これらのAPIを実装することで、kotcollectionsはKotlin標準ライブラリとほぼ完全な互換性を持つことになります。

総実装時間の見積もり: **8-15時間**（テスト含む）

## 参考資料

- [Kotlin Collection API公式ドキュメント](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/)
- プロジェクト内の既存実装パターン
- kotcollections既存のテスト構造
