"""Unit tests for PulseQ patient records and linked-list operations."""

import unittest

from pulseq.models import Patient
from pulseq.patient_store import PatientLinkedList


def patient(patient_id: str = "P001", name: str = "Asha", age: int = 20) -> Patient:
    return Patient(
        patient_id=patient_id,
        name=name,
        age=age,
        sex="Female",
        contact="demo@example.test",
        reason="Routine check-up",
    )


class PatientModelTests(unittest.TestCase):
    def test_id_is_trimmed_and_normalised(self) -> None:
        self.assertEqual(patient(" p-01 ").patient_id, "P-01")

    def test_rejects_invalid_age(self) -> None:
        with self.assertRaises(ValueError):
            patient(age=-1)
        with self.assertRaises(ValueError):
            patient(age=131)

    def test_update_validates_before_mutating(self) -> None:
        item = patient()
        with self.assertRaises(ValueError):
            item.update(name="Updated", age=-3)
        self.assertEqual(item.name, "Asha")
        self.assertEqual(item.age, 20)


class PatientLinkedListTests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = PatientLinkedList()

    def test_empty_list(self) -> None:
        self.assertEqual(len(self.records), 0)
        self.assertEqual(self.records.view_all(), [])
        self.assertIsNone(self.records.find("missing"))

    def test_register_and_preserve_insertion_order(self) -> None:
        self.records.register(patient("P1", "Asha"))
        self.records.register(patient("P2", "Bala"))
        self.assertEqual([p.patient_id for p in self.records], ["P1", "P2"])
        self.assertEqual(len(self.records), 2)

    def test_duplicate_ids_are_case_insensitive(self) -> None:
        self.records.register(patient("p01"))
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.records.register(patient("P01", "Duplicate"))
        self.assertEqual(len(self.records), 1)

    def test_find_is_case_insensitive(self) -> None:
        self.records.register(patient("P01"))
        self.assertEqual(self.records.find(" p01 ").name, "Asha")

    def test_update_existing_and_reject_missing(self) -> None:
        self.records.register(patient("P01"))
        updated = self.records.update("p01", name="Asha K", age=21)
        self.assertEqual((updated.name, updated.age), ("Asha K", 21))
        with self.assertRaises(KeyError):
            self.records.update("MISSING", name="Nobody")

    def test_invalid_update_does_not_partially_change_record(self) -> None:
        self.records.register(patient("P01"))
        with self.assertRaises(ValueError):
            self.records.update("P01", name="New Name", age=-1)
        self.assertEqual(self.records.find("P01").name, "Asha")

    def test_delete_head_middle_tail_and_missing(self) -> None:
        for key in ("P1", "P2", "P3"):
            self.records.register(patient(key, key))
        self.assertEqual(self.records.delete("P1").patient_id, "P1")
        self.assertEqual(self.records.delete("P2").patient_id, "P2")
        self.assertEqual(self.records.delete("P3").patient_id, "P3")
        self.assertEqual(len(self.records), 0)
        self.assertEqual(self.records.view_all(), [])
        with self.assertRaises(KeyError):
            self.records.delete("P3")

    def test_clear_resets_list(self) -> None:
        self.records.register(patient())
        self.records.clear()
        self.assertEqual(len(self.records), 0)
        self.assertFalse(self.records)


if __name__ == "__main__":
    unittest.main()
