"""Unit tests for PulseQ's manual merge sort and insertion sort."""

import unittest

from pulseq.models import Patient
from pulseq.sorting import insertion_sort, merge_sort


def patient(patient_id: str, name: str, age: int) -> Patient:
    return Patient(
        patient_id=patient_id,
        name=name,
        age=age,
        sex="Not specified",
        contact="demo@example.test",
        reason="Demonstration",
    )


class SortingTests(unittest.TestCase):
    def test_both_algorithms_sort_numbers(self) -> None:
        values = [7, 2, 9, 1, 5, 2]
        self.assertEqual(merge_sort(values), [1, 2, 2, 5, 7, 9])
        self.assertEqual(insertion_sort(values), [1, 2, 2, 5, 7, 9])

    def test_empty_and_single_item_sequences(self) -> None:
        for algorithm in (merge_sort, insertion_sort):
            self.assertEqual(algorithm([]), [])
            self.assertEqual(algorithm([4]), [4])

    def test_already_sorted_and_reverse_sorted(self) -> None:
        for algorithm in (merge_sort, insertion_sort):
            self.assertEqual(algorithm([1, 2, 3, 4]), [1, 2, 3, 4])
            self.assertEqual(algorithm([4, 3, 2, 1]), [1, 2, 3, 4])

    def test_reverse_order(self) -> None:
        for algorithm in (merge_sort, insertion_sort):
            self.assertEqual(algorithm([3, 1, 4, 2], reverse=True), [4, 3, 2, 1])

    def test_patient_sort_by_normalized_id_supports_binary_search(self) -> None:
        records = [patient("P30", "Zara", 30), patient("P10", "Asha", 20), patient("P20", "Bala", 25)]
        for algorithm in (merge_sort, insertion_sort):
            sorted_records = algorithm(records, key=lambda p: p.patient_id)
            self.assertEqual([p.patient_id for p in sorted_records], ["P10", "P20", "P30"])

    def test_sort_patients_by_name_case_insensitively(self) -> None:
        records = [patient("P1", "zara", 19), patient("P2", "Asha", 20), patient("P3", "bala", 21)]
        for algorithm in (merge_sort, insertion_sort):
            self.assertEqual(
                [p.name for p in algorithm(records, key=lambda p: p.name.casefold())],
                ["Asha", "bala", "zara"],
            )

    def test_sort_patients_by_age(self) -> None:
        records = [patient("P1", "Zara", 30), patient("P2", "Asha", 18), patient("P3", "Bala", 25)]
        for algorithm in (merge_sort, insertion_sort):
            self.assertEqual(
                [p.age for p in algorithm(records, key=lambda p: p.age)],
                [18, 25, 30],
            )

    def test_duplicate_keys_preserve_input_order(self) -> None:
        records = [
            {"name": "A", "age": 20},
            {"name": "B", "age": 18},
            {"name": "C", "age": 20},
            {"name": "D", "age": 18},
        ]
        for algorithm in (merge_sort, insertion_sort):
            sorted_records = algorithm(records, key=lambda item: item["age"])
            self.assertEqual([item["name"] for item in sorted_records], ["B", "D", "A", "C"])

    def test_input_sequence_is_not_mutated(self) -> None:
        original = [3, 1, 2]
        for algorithm in (merge_sort, insertion_sort):
            self.assertEqual(algorithm(original), [1, 2, 3])
            self.assertEqual(original, [3, 1, 2])

    def test_invalid_collection_is_rejected(self) -> None:
        for algorithm in (merge_sort, insertion_sort):
            with self.assertRaises(TypeError):
                algorithm(None)  # type: ignore[arg-type]

    def test_key_is_applied_and_bad_keys_raise(self) -> None:
        for algorithm in (merge_sort, insertion_sort):
            self.assertEqual(algorithm(["bbb", "a", "cc"], key=len), ["a", "cc", "bbb"])
            with self.assertRaises(TypeError):
                algorithm([1, "two"], key=lambda value: value)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
