"""Custom queue structures for PulseQ.

The routine queue is implemented with linked nodes and does not use
collections.deque or any other built-in queue implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from pulseq.models import Patient


@dataclass
class _QueueNode:
    patient: Patient
    next: _QueueNode | None = None


class RoutineQueue:
    """First-in-first-out queue for routine patients.

    enqueue() adds at the tail and dequeue() removes from the head. Both are
    O(1). This queue models routine flow only; emergency cases will use a
    separate priority queue in a later milestone.
    """

    def __init__(self) -> None:
        self._head: _QueueNode | None = None
        self._tail: _QueueNode | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._head is not None

    def is_empty(self) -> bool:
        """Return True when no routine patients are waiting. O(1)."""
        return self._head is None

    def __iter__(self) -> Iterator[Patient]:
        current = self._head
        while current is not None:
            yield current.patient
            current = current.next

    def enqueue(self, patient: Patient) -> None:
        """Add a patient to the end of the queue. O(1)."""
        if not isinstance(patient, Patient):
            raise TypeError("enqueue() expects a Patient instance.")

        node = _QueueNode(patient)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self) -> Patient:
        """Remove and return the next patient. Raises IndexError if empty."""
        if self._head is None:
            raise IndexError("Cannot dequeue from an empty routine queue.")

        node = self._head
        self._head = node.next
        self._size -= 1

        if self._head is None:
            self._tail = None

        return node.patient

    def peek(self) -> Patient:
        """Return the next patient without removing them."""
        if self._head is None:
            raise IndexError("Cannot peek at an empty routine queue.")
        return self._head.patient

    def view_all(self) -> list[Patient]:
        """Return a snapshot of queued patients in FIFO order. O(n)."""
        return list(self)

    def clear(self) -> None:
        """Remove all queued patients. O(1)."""
        self._head = self._tail = None
        self._size = 0
