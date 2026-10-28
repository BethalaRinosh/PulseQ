"""Patient record storage implemented with a custom singly linked list.

The list is intentionally implemented directly for DSA learning. It does not
use a built-in list as the patient-record container.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from pulseq.models import Patient


@dataclass
class _Node:
    patient: Patient
    next: _Node | None = None


class PatientLinkedList:
    """Singly linked list supporting patient CRUD and duplicate-ID protection.

    Patient IDs are compared case-insensitively. The list preserves insertion
    order. This implementation is in-memory only; records disappear on exit.
    """

    def __init__(self) -> None:
        self._head: _Node | None = None
        self._tail: _Node | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._head is not None

    def __iter__(self) -> Iterator[Patient]:
        current = self._head
        while current is not None:
            yield current.patient
            current = current.next

    @staticmethod
    def _normalise_id(patient_id: str) -> str:
        if not isinstance(patient_id, str) or not patient_id.strip():
            raise ValueError("Patient ID cannot be empty.")
        return patient_id.strip().upper()

    def find(self, patient_id: str) -> Patient | None:
        """Return a patient by ID, or None if no matching record exists. O(n)."""
        target = self._normalise_id(patient_id)
        current = self._head
        while current is not None:
            if current.patient.patient_id == target:
                return current.patient
            current = current.next
        return None

    def register(self, patient: Patient) -> None:
        """Append a patient in O(1); reject duplicate IDs after an O(n) scan."""
        if not isinstance(patient, Patient):
            raise TypeError("register() expects a Patient instance.")
        if self.find(patient.patient_id) is not None:
            raise ValueError(f"Patient ID '{patient.patient_id}' already exists.")

        node = _Node(patient)
        if self._head is None:
            self._head = self._tail = node
        else:
            assert self._tail is not None
            self._tail.next = node
            self._tail = node
        self._size += 1

    def view_all(self) -> list[Patient]:
        """Return a snapshot of records in insertion order. O(n)."""
        return list(self)

    def update(self, patient_id: str, **changes: object) -> Patient:
        """Update allowed fields of an existing patient; return the record."""
        patient = self.find(patient_id)
        if patient is None:
            raise KeyError(f"No patient found with ID '{self._normalise_id(patient_id)}'.")
        patient.update(**changes)
        return patient

    def delete(self, patient_id: str) -> Patient:
        """Remove and return a patient by ID. O(n)."""
        target = self._normalise_id(patient_id)
        previous: _Node | None = None
        current = self._head

        while current is not None:
            if current.patient.patient_id == target:
                if previous is None:
                    self._head = current.next
                else:
                    previous.next = current.next

                if current is self._tail:
                    self._tail = previous

                self._size -= 1
                if self._size == 0:
                    self._head = self._tail = None
                return current.patient

            previous, current = current, current.next

        raise KeyError(f"No patient found with ID '{target}'.")

    def clear(self) -> None:
        """Remove all records and release the linked nodes."""
        self._head = self._tail = None
        self._size = 0
