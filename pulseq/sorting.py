"""Manual, stable sorting algorithms for PulseQ.

Both algorithms return a new list and leave the input sequence unchanged.
They accept an optional key function and a reverse flag. No built-in sorting
helpers are used.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")


def merge_sort(
    items: Sequence[T],
    *,
    key: Callable[[T], K] | None = None,
    reverse: bool = False,
) -> list[T]:
    """Return a stable merge-sorted copy of items.

    Time: O(n log n) in best, average, and worst cases.
    Extra space: O(n).
    """
    if not isinstance(items, Sequence):
        raise TypeError("items must be a sequence.")
    key_fn: Callable[[T], object] = key if key is not None else (lambda item: item)
    source = list(items)
    for item in source:
        key_fn(item)

    def merge(left: list[T], right: list[T]) -> list[T]:
        merged: list[T] = []
        i = j = 0
        while i < len(left) and j < len(right):
            left_key = key_fn(left[i])
            right_key = key_fn(right[j])
            if (left_key >= right_key) if reverse else (left_key <= right_key):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    def split_and_sort(values: list[T]) -> list[T]:
        if len(values) <= 1:
            return values
        middle = len(values) // 2
        return merge(split_and_sort(values[:middle]), split_and_sort(values[middle:]))

    return split_and_sort(source)


def insertion_sort(
    items: Sequence[T],
    *,
    key: Callable[[T], K] | None = None,
    reverse: bool = False,
) -> list[T]:
    """Return a stable insertion-sorted copy of items.

    Time: O(n) best case, O(n²) average and worst cases.
    Extra space: O(n) for the returned copy; O(1) auxiliary algorithm space.
    """
    if not isinstance(items, Sequence):
        raise TypeError("items must be a sequence.")
    key_fn: Callable[[T], object] = key if key is not None else (lambda item: item)
    result = list(items)
    for item in result:
        key_fn(item)

    for index in range(1, len(result)):
        current = result[index]
        current_key = key_fn(current)
        position = index - 1
        while position >= 0:
            previous_key = key_fn(result[position])
            should_shift = previous_key < current_key if reverse else previous_key > current_key
            if not should_shift:
                break
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
    return result
