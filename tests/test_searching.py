"""Unit tests for PulseQ's manual linear and binary search algorithms."""

import unittest

from pulseq.models import Patient
from pulseq.searching import binary_search_by_id, linear_search_by_id, linear_search_by_name


def patient(patient_id: str, name: str, age: int = 20) -> Patient:
    return Patient(
        patient_id=patient_id,
        name=name,
        age=age,
        sex="Not specified",
        contact="demo@example.test",
        reason="Demonstration",
    )


class LinearSearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = [
            patient("P030", "Asha Rao"),
            patient("P010", "Bala"),
            patient("P020", "Asha Menon"),
        ]

    def test_find_id_without_requiring_sorted_input(self) -> None:
        self.assertEqual(linear_search_by_id(self.records, " p010 ").name, "Bala")

    def test_missing_id_returns_none(self) -> None:
        self.assertIsNone(linear_search_by_id(self.records, "P999"))

    def test_empty_id_query_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            linear_search_by_id(self.records, "  ")

    def test_name_search_is_case_insensitive_and_partial(self) -> None:
        found = linear_search_by_name(self.records, "ASHA")
        self.assertEqual([p.patient_id for p in found], ["P030", "P020"])

    def test_duplicate_names_return_all_matches_in_input_order(self) -> None:
        records = [patient("P1", "Sam Lee"), patient("P2", "SAM LEE"), patient("P3", "Sam")]
        found = linear_search_by_name(records, "sam lee")
        self.assertEqual([p.patient_id for p in found], ["P1", "P2"])

    def test_missing_name_returns_empty_list(self) -> None:
        self.assertEqual(linear_search_by_name(self.records, "Nobody"), [])

    def test_empty_name_query_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            linear_search_by_name(self.records, "")

    def test_empty_collection(self) -> None:
        self.assertIsNone(linear_search_by_id([], "P1"))
        self.assertEqual(linear_search_by_name([], "Asha"), [])

    def test_wrong_collection_or_record_type_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            linear_search_by_id(None, "P1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            linear_search_by_name([object()], "Asha")  # type: ignore[list-item]


class BinarySearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sorted_records = [
            patient("P010", "Bala"),
            patient("P020", "Asha"),
            patient("P030", "Chandra"),
            patient("P040", "Deepa"),
            patient("P050", "Esha"),
        ]

    def test_find_first_middle_and_last_positions(self) -> None:
        self.assertEqual(binary_search_by_id(self.sorted_records, "p010").name, "Bala")
        self.assertEqual(binary_search_by_id(self.sorted_records, "P030").name, "Chandra")
        self.assertEqual(binary_search_by_id(self.sorted_records, "P050").name, "Esha")

    def test_missing_ids_before_between_and_after_range(self) -> None:
        for missing in ("P001", "P025", "P999"):
            with self.subTest(missing=missing):
                self.assertIsNone(binary_search_by_id(self.sorted_records, missing))

    def test_empty_collection(self) -> None:
        self.assertIsNone(binary_search_by_id([], "P1"))

    def test_empty_query_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            binary_search_by_id(self.sorted_records, " ")

    def test_wrong_collection_or_record_type_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            binary_search_by_id(None, "P1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            binary_search_by_id([object()], "P1")  # type: ignore[list-item]


if __name__ == "__main__":
    unittest.main()
