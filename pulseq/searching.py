"""Manual patient-search algorithms for PulseQ.

Linear search works on any patient sequence. Binary search requires the input
sequence to already be sorted by patient_id in ascending normalized order.
The algorithms are implemented directly for DSA learning; no bisect helpers
are used.
"""

from __future__ import annotations

from collections.abc import Sequence

from pulseq.models import Patient


def _normalise_query(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()


def linear_search_by_id(patients: Sequence[Patient], patient_id: str) -> Patient | None:
    """Find a patient by ID in any order. O(n) time, O(1) extra space."""
    if not isinstance(patients, Sequence):
        raise TypeError("patients must be a sequence of Patient records.")
    target = _normalise_query(patient_id, "Patient ID").upper()
    for patient in patients:
        if not isinstance(patient, Patient):
            raise TypeError("patients must contain only Patient records.")
        if patient.patient_id == target:
            return patient
    return None


def linear_search_by_name(patients: Sequence[Patient], name_query: str) -> list[Patient]:
    """Return every patient whose name contains the query, case-insensitively.

    Duplicate names are allowed and all matches are returned in input order.
    O(n) time and O(k) output space, where k is the number of matches.
    """
    if not isinstance(patients, Sequence):
        raise TypeError("patients must be a sequence of Patient records.")
    target = _normalise_query(name_query, "Name query").casefold()
    matches: list[Patient] = []
    for patient in patients:
        if not isinstance(patient, Patient):
            raise TypeError("patients must contain only Patient records.")
        if target in patient.name.casefold():
            matches.append(patient)
    return matches


def binary_search_by_id(
    sorted_patients: Sequence[Patient], patient_id: str
) -> Patient | None:
    """Find an ID in records sorted ascending by normalized patient_id.

    The sorted-input requirement is a precondition. This function deliberately
    does not sort or scan the sequence to validate ordering, preserving O(log n)
    search time and O(1) extra space. Returns None when the ID is absent.
    """
    if not isinstance(sorted_patients, Sequence):
        raise TypeError("sorted_patients must be a sequence of Patient records.")
    target = _normalise_query(patient_id, "Patient ID").upper()
    low = 0
    high = len(sorted_patients) - 1

    while low <= high:
        middle = low + (high - low) // 2
        patient = sorted_patients[middle]
        if not isinstance(patient, Patient):
            raise TypeError("sorted_patients must contain only Patient records.")
        if patient.patient_id == target:
            return patient
        if patient.patient_id < target:
            low = middle + 1
        else:
            high = middle - 1
    return None
