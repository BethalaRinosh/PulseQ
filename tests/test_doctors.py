"""Unit tests for doctor registration and specialization-aware allocation."""

import unittest

from pulseq.doctors import Doctor, DoctorDirectory
from pulseq.models import Patient


def doctor(
    doctor_id: str = "D001",
    name: str = "Dr Asha",
    specialization: str = "Cardiology",
    available: bool = True,
) -> Doctor:
    return Doctor(
        doctor_id=doctor_id,
        name=name,
        specialization=specialization,
        contact="demo@example.test",
        available=available,
    )


def patient(patient_id: str = "P001") -> Patient:
    return Patient(
        patient_id=patient_id,
        name="Demo Patient",
        age=30,
        sex="Unspecified",
        contact="demo@example.test",
        reason="Demo appointment",
    )


class DoctorModelTests(unittest.TestCase):
    def test_normalises_id_and_trims_text(self) -> None:
        item = doctor(" d-01 ", " Dr Asha ", " Cardiology ")
        self.assertEqual(item.doctor_id, "D-01")
        self.assertEqual(item.name, "Dr Asha")
        self.assertEqual(item.specialization, "Cardiology")

    def test_doctor_id_is_immutable(self) -> None:
        item = doctor()
        with self.assertRaisesRegex(AttributeError, "immutable"):
            item.doctor_id = "D999"
        self.assertEqual(item.doctor_id, "D001")

    def test_direct_availability_assignment_rejects_non_boolean(self) -> None:
        item = doctor()
        with self.assertRaisesRegex(ValueError, "availability"):
            item.available = 1
        self.assertTrue(item.available)

    def test_rejects_invalid_fields_and_availability(self) -> None:
        for kwargs in (
            {"doctor_id": " ", "name": "Doc", "specialization": "Cardiology", "contact": "x"},
            {"doctor_id": "D1", "name": "", "specialization": "Cardiology", "contact": "x"},
            {"doctor_id": "D1", "name": "Doc", "specialization": " ", "contact": "x"},
            {"doctor_id": "D1", "name": "Doc", "specialization": "Cardiology", "contact": " "},
            {"doctor_id": "D1", "name": "Doc", "specialization": "Cardiology", "contact": "x", "available": 1},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    Doctor(**kwargs)


class DoctorDirectoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = DoctorDirectory()

    def test_empty_directory_and_view_snapshot(self) -> None:
        self.assertFalse(self.directory)
        self.assertEqual(len(self.directory), 0)
        self.assertEqual(self.directory.view_all(), [])
        self.assertIsNone(self.directory.find("missing"))

    def test_register_find_and_reject_duplicate_ids(self) -> None:
        self.directory.register(doctor("d01"))
        self.assertEqual(self.directory.find(" D01 ").name, "Dr Asha")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.directory.register(doctor("D01", "Duplicate"))
        self.assertEqual(len(self.directory), 1)

    def test_rejects_non_doctor_records(self) -> None:
        with self.assertRaises(TypeError):
            self.directory.register("not a doctor")  # type: ignore[arg-type]

    def test_matches_specialization_case_insensitively(self) -> None:
        self.directory.register(doctor("D1", specialization="Cardiology"))
        assigned = self.directory.allocate_patient(patient(), "  CARDIOLOGY ")
        self.assertEqual(assigned.doctor_id, "D1")

    def test_skips_unavailable_doctors(self) -> None:
        self.directory.register(doctor("D1", available=False))
        self.directory.register(doctor("D2", name="Dr Bala"))
        assigned = self.directory.allocate_patient(patient(), "Cardiology")
        self.assertEqual(assigned.doctor_id, "D2")

    def test_returns_none_when_no_available_specialist_exists(self) -> None:
        self.directory.register(doctor("D1", specialization="Neurology"))
        self.directory.register(doctor("D2", specialization="Cardiology", available=False))
        self.assertIsNone(self.directory.allocate_patient(patient(), "Cardiology"))

    def test_allocates_to_least_loaded_doctor_and_breaks_ties_by_registration(self) -> None:
        self.directory.register(doctor("D1"))
        self.directory.register(doctor("D2", name="Dr Bala"))
        self.assertEqual(self.directory.allocate_patient(patient("P1"), "Cardiology").doctor_id, "D1")
        self.assertEqual(self.directory.allocate_patient(patient("P2"), "Cardiology").doctor_id, "D2")
        self.assertEqual(self.directory.allocate_patient(patient("P3"), "Cardiology").doctor_id, "D1")
        self.assertEqual((self.directory.find("D1").current_load, self.directory.find("D2").current_load), (2, 1))

    def test_prevents_duplicate_active_patient_assignment(self) -> None:
        self.directory.register(doctor())
        self.directory.allocate_patient(patient("P1"), "Cardiology")
        with self.assertRaisesRegex(ValueError, "already has an active"):
            self.directory.allocate_patient(patient("p1"), "Cardiology")
        self.assertEqual(self.directory.find("D001").current_load, 1)

    def test_release_patient_updates_load_and_allows_reassignment(self) -> None:
        self.directory.register(doctor("D1"))
        self.directory.register(doctor("D2", name="Dr Bala"))
        self.directory.allocate_patient(patient("P1"), "Cardiology")
        released = self.directory.release_patient(" p1 ")
        self.assertEqual(released.doctor_id, "D1")
        self.assertEqual(released.current_load, 0)
        self.assertIsNone(self.directory.assigned_doctor("P1"))
        reassigned = self.directory.allocate_patient(patient("P1"), "Cardiology")
        self.assertEqual(reassigned.doctor_id, "D1")

    def test_rejects_unknown_doctor_and_invalid_availability(self) -> None:
        with self.assertRaises(KeyError):
            self.directory.set_availability("D404", False)
        with self.assertRaises(ValueError):
            self.directory.set_availability("D1", 1)  # type: ignore[arg-type]
        self.directory.register(doctor("D1"))
        self.assertFalse(self.directory.set_availability("d1", False).available)

    def test_release_unknown_patient_raises(self) -> None:
        with self.assertRaises(KeyError):
            self.directory.release_patient("P404")

    def test_clear_resets_records_and_assignment_state(self) -> None:
        self.directory.register(doctor())
        self.directory.allocate_patient(patient(), "Cardiology")
        self.directory.clear()
        self.assertEqual(len(self.directory), 0)
        self.assertFalse(self.directory)
        self.assertEqual(self.directory.view_all(), [])
