# Kotlin互換性差分レポート (2025-09-04)

本レポートは、kotcollections（KotList/KotSet/KotMap など）の挙動をKotlin標準ライブラリと比較し、相違点（互換性ギャップ）を整理したものです。直近で KotList.intersect/union/subtract は Kotlin準拠（Set返却）に変更済みです。それ以外の差分と是正案を以下にまとめます。

## サマリー

優先度の高い差分:
- KotList.minus の削除挙動（単一要素・複数要素）
- KotSet.map/filter/flat_map/map_indexed/flat_map_indexed の返却型（Set→List）
- KotSet.group_by の値型（Set→List）

中〜低優先度:
- empty の average の扱い（例外 vs NaN）
- 例外クラスの種類（Python流 vs Kotlin流）
- KotList.flatten の対象（Python的拡張）
- KotList.plus のKotMap/KotSet対応（拡張仕様）

## 差分詳細

### 1) KotList.minus の削除挙動（優先度: 高）
- 現状:
  - 単一要素版: 最初の1個だけ削除
  - Iterable版: 集合差（set化）で全出現を削除（多重度を無視）
- Kotlin期待:
  - 単一要素版: 対象と等しい全要素を削除
  - Iterable版: 出現回数ベースの多重度削減（マルチセット差）
- 例:
```python path=null start=null
# Kotlin
listOf(1,2,2,3).minus(2)          # [1,3]
listOf(1,2,2,3).minus(listOf(2))  # [1,2,3]
listOf(1,2,2,3).minus(listOf(2,2))# [1,3]

# 現状
KotList([1,2,2,3]).minus(2).to_list()       # [1,2,3]
KotList([1,2,2,3]).minus([2]).to_list()     # [1,3]
KotList([1,2,2,3]).minus([2,2]).to_list()   # [1,3]
```
- 是正案:
  - 単一要素: 全削除に変更
  - Iterable版: collections.Counter などを用いて多重度差を実装
- 影響: 互換性改善。既存の一部テスト・ユーザーコードに影響の可能性あり（破壊的ではないが挙動変化）。
- 対象ファイル: kotcollections/kot_list.py（minus）

### 2) KotSet.map / filter / flat_map / map_indexed / flat_map_indexed の返却型（優先度: 高）
- 現状: KotSet を返す（重複が消える・順序非保証）
- Kotlin期待: List を返す（Iterable拡張のため）
- 例:
```python path=null start=null
# Kotlin
setOf(1,2,3).map { it % 2 }  # [1,0,1]

# 現状（重複消失）
KotSet([1,2,3]).map(lambda x: x % 2).to_list()  # [0,1] など
```
- 是正案:
  - 返却型を KotList に変更（Kotlin準拠）。もしくは互換性保持のため、現行メソッドは残し map_to_set 等の別名に分離（推奨はKotlin準拠へ寄せる）。
- 影響: 破壊的変更。テスト・ドキュメント更新要。
- 対象ファイル: kotcollections/kot_set.py（map/filter/flat_map 系）

### 3) KotSet.group_by の値型（優先度: 中〜高）
- 現状: KotMap<K, KotSet<T>>
- Kotlin期待: Map<K, List<T>>
- 是正案: KotList を値として返すよう変更
- 影響: 破壊的変更。テスト・ドキュメント更新要。
- 対象ファイル: kotcollections/kot_set.py（group_by）

### 4) empty の average の扱い（優先度: 中）
- 現状: KotList.average() / KotSet.average(selector) は空で ValueError を送出
- Kotlin期待: NaN（Double.NaN）
- 是正案:
  - Pythonでは float('nan') を返す
  - 互換性を優先しない場合は現状のまま＋ドキュメントに相違を明記
- 影響: 仕様変更（非例外化）。下流の例外依存コードに影響の可能性。
- 対象ファイル: kotcollections/kot_list.py（average）、kotcollections/kot_set.py（average）

### 5) 例外クラスの違い（優先度: 低〜中）
- 代表例（Kotlin → 現状）:
  - IndexOutOfBoundsException → IndexError（element_at など）
  - NoSuchElementException → IndexError（first/last）
  - IllegalArgumentException → ValueError（single）
  - UnsupportedOperationException → ValueError（reduce on empty）
  - NoSuchElementException（Map.getValue）→ KeyError
- 是正案: 完全互換を目指すなら独自例外を用意して置換。実用上は現状でも問題は軽微と考える。

### 6) KotList.flatten の対象（優先度: 低）
- 現状: ランタイムで Iterable なら展開、非Iterable はそのまま（Python的拡張）
- Kotlin期待: List<Iterable<T>> 前提（型で担保）
- 是正案: 現状維持でOK。差分は仕様としてドキュメント化。

### 7) KotList.plus の拡張対応（優先度: 低）
- 現状: KotMap/KotSet を渡したときの扱いを便利仕様として拡張（KotMapは values を結合等）
- Kotlin期待: そのような特殊取扱いはない
- 是正案: 現状維持（利便性向上）。Kotlinとの差分としてドキュメント化。

## 既にKotlin準拠化済み（2025-09-04）
- KotList.intersect/union/subtract は KotSet を返すように修正済み（Kotlin準拠）。

## 推奨修正順（提案）
1. KotList.minus の多重度仕様（単一・Iterable）をKotlin準拠に修正（破壊性: 中）
2. KotSet.map/filter 系の返却型を KotList へ（破壊性: 高）
3. KotSet.group_by の値型を KotList へ（破壊性: 中）
4. average(empty) を NaN へ（破壊性: 低〜中）
5. 例外型はドキュメント明記 or ラッパ導入（任意）

## テスト更新方針（要点）
- minus: 多重度テスト（単一・複数・同値2個以上・順序保持）
- KotSet.map/filter: 返却型が KotList であること、重複の保持、順序の検証
- KotSet.group_by: 値が KotList であること、要素数・内容を検証
- average: 空入力で math.isnan を検証

## 備考
- Python流の例外・動的型の文脈に最適化した現行挙動も一定の合理性はありますが、「Kotlin互換」を明確な目標とする場合は本レポートの修正案が有効です。

