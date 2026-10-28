"""Custom binary max-heap for emergency patient prioritisation.

Urgency is an educational integer score from 1 (lower) to 5 (higher).
This is not a clinical triage scale. Equal urgency is served FIFO.
"""

from __future__ import annotations

from dataclasses import dataclass
from pulseq.models import Patient


MIN_URGENCY = 1
MAX_URGENCY = 5


@dataclass(frozen=True)
class EmergencyCase:
    """A patient and their demonstration urgency score."""

    patient: Patient
    urgency: int
    arrival_order: int


class EmergencyPriorityQueue:
    """Binary max-heap with FIFO tie-breaking for equal urgency.

    The heap is implemented directly with a Python list. Higher urgency scores
    have higher priority; when scores tie, the smaller arrival_order wins.
    """

    def __init__(self) -> None:
        self._heap: list[EmergencyCase] = []
        self._next_arrival_order = 0

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def is_empty(self) -> bool:
        """Return True if no emergency cases are waiting. O(1)."""
        return not self._heap

    @staticmethod
    def _has_higher_priority(left: EmergencyCase, right: EmergencyCase) -> bool:
        """Return True if left should be served before right."""
        if left.urgency != right.urgency:
            return left.urgency > right.urgency
        return left.arrival_order < right.arrival_order

    @staticmethod
    def _validate(patient: Patient, urgency: int) -> None:
        if not isinstance(patient, Patient):
            raise TypeError("enqueue() expects a Patient instance.")
        if isinstance(urgency, bool) or not isinstance(urgency, int):
            raise ValueError("Urgency must be an integer from 1 to 5.")
        if not MIN_URGENCY <= urgency <= MAX_URGENCY:
            raise ValueError("Urgency must be an integer from 1 to 5.")

    def enqueue(self, patient: Patient, urgency: int) -> None:
        """Insert an emergency case and restore the heap. O(log n)."""
        self._validate(patient, urgency)
        entry = EmergencyCase(patient, urgency, self._next_arrival_order)
        self._next_arrival_order += 1
        self._heap.append(entry)

        child = len(self._heap) - 1
        while child > 0:
            parent = (child - 1) // 2
            if not self._has_higher_priority(self._heap[child], self._heap[parent]):
                break
            self._heap[child], self._heap[parent] = self._heap[parent], self._heap[child]
            child = parent

    def peek(self) -> EmergencyCase:
        """Return the highest-priority case without removing it. O(1)."""
        if not self._heap:
            raise IndexError("Cannot peek at an empty emergency priority queue.")
        return self._heap[0]

    def dequeue(self) -> EmergencyCase:
        """Remove and return the highest-priority case. O(log n)."""
        if not self._heap:
            raise IndexError("Cannot dequeue from an empty emergency priority queue.")

        highest = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            parent = 0
            size = len(self._heap)

            while True:
                left = 2 * parent + 1
                right = left + 1
                best = parent

                if left < size and self._has_higher_priority(
                    self._heap[left], self._heap[best]
                ):
                    best = left
                if right < size and self._has_higher_priority(
                    self._heap[right], self._heap[best]
                ):
                    best = right
                if best == parent:
                    break

                self._heap[parent], self._heap[best] = (
                    self._heap[best],
                    self._heap[parent],
                )
                parent = best

        return highest

    def view_all(self) -> list[EmergencyCase]:
        """Return a priority-ordered snapshot without changing the heap. O(n log n)."""
        copy = EmergencyPriorityQueue()
        copy._heap = self._heap.copy()
        copy._next_arrival_order = self._next_arrival_order
        ordered: list[EmergencyCase] = []
        while copy:
            ordered.append(copy.dequeue())
        return ordered

    def clear(self) -> None:
        """Remove all waiting cases. O(n) to release stored references."""
        self._heap.clear()
