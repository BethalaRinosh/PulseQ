"""Doctor directory and specialization-aware patient allocation.

This is an in-memory academic simulation. Allocation is administrative only and
must not be interpreted as clinical decision support.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pulseq.models import Patient


@dataclass
class Doctor:
    """A doctor record for the PulseQ demonstration."""

    doctor_id: str
    name: str
    specialization: str
    contact: str
    available: bool = True
    _current_load: int = field(default=0, init=False, repr=False, compare=False)

    def __setattr__(self, name: str, value: object) -> None:
        if name == "doctor_id" and "doctor_id" in self.__dict__:
            raise AttributeError("Doctor ID is immutable after construction.")
        if name == "available" and not isinstance(value, bool):
            raise ValueError("Doctor availability must be True or False.")
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        object.__setattr__(self, "doctor_id", self._required_text(self.doctor_id, "Doctor ID").upper())
        self.name = self._required_text(self.name, "Doctor name")
        self.specialization = self._required_text(self.specialization, "Specialization")
        self.contact = self._required_text(self.contact, "Doctor contact")
        if not isinstance(self.available, bool):
            raise ValueError("Doctor availability must be True or False.")

    @staticmethod
    def _required_text(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return value.strip()

    @property
    def current_load(self) -> int:
        """Number of active demo assignments currently held by this doctor."""
        return self._current_load


class DoctorDirectory:
    """Array-backed doctor directory with simple load-aware allocation.

    Doctors are stored in a Python list, as allowed for the doctor directory.
    For a requested specialization, allocation chooses an available doctor
    with the smallest active assignment count. Ties preserve registration
    order. A patient can have at most one active doctor assignment.
    """

    def __init__(self) -> None:
        self._doctors: list[Doctor] = []
        self._assignments: dict[str, str] = {}

    def __len__(self) -> int:
        return len(self._doctors)

    def __bool__(self) -> bool:
        return bool(self._doctors)

    @staticmethod
    def _normalise_id(identifier: str, field_name: str = "Doctor ID") -> str:
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return identifier.strip().upper()

    @staticmethod
    def _normalise_specialization(specialization: str) -> str:
        if not isinstance(specialization, str) or not specialization.strip():
            raise ValueError("Specialization cannot be empty.")
        return specialization.strip().casefold()

    def register(self, doctor: Doctor) -> None:
        """Register a doctor, rejecting duplicate IDs. O(d)."""
        if not isinstance(doctor, Doctor):
            raise TypeError("register() expects a Doctor instance.")
        if self.find(doctor.doctor_id) is not None:
            raise ValueError(f"Doctor ID '{doctor.doctor_id}' already exists.")
        self._doctors.append(doctor)

    def find(self, doctor_id: str) -> Doctor | None:
        """Find a doctor by ID, case-insensitively. O(d)."""
        target = self._normalise_id(doctor_id)
        for doctor in self._doctors:
            if doctor.doctor_id == target:
                return doctor
        return None

    def view_all(self) -> list[Doctor]:
        """Return a registration-ordered snapshot of doctor references. O(d)."""
        return list(self._doctors)

    def set_availability(self, doctor_id: str, available: bool) -> Doctor:
        """Change availability; current assignments are not cancelled."""
        if not isinstance(available, bool):
            raise ValueError("Doctor availability must be True or False.")
        doctor = self.find(doctor_id)
        if doctor is None:
            raise KeyError(f"No doctor found with ID '{self._normalise_id(doctor_id)}'.")
        doctor.available = available
        return doctor

    def allocate_patient(self, patient: Patient, specialization: str) -> Doctor | None:
        """Assign a patient to the least-loaded available matching doctor.

        Returns None when no available doctor matches. Raises ValueError if
        this patient already has an active assignment. Selection ties preserve
        doctor registration order. This is a scheduling demonstration only.
        """
        if not isinstance(patient, Patient):
            raise TypeError("allocate_patient() expects a Patient instance.")
        requested = self._normalise_specialization(specialization)
        if patient.patient_id in self._assignments:
            raise ValueError(
                f"Patient ID {patient.patient_id} already has an active doctor assignment."
            )

        candidates = [
            doctor for doctor in self._doctors
            if doctor.available and doctor.specialization.casefold() == requested
        ]
        if not candidates:
            return None

        selected = candidates[0]
        for doctor in candidates[1:]:
            if doctor.current_load < selected.current_load:
                selected = doctor

        self._assignments[patient.patient_id] = selected.doctor_id
        selected._current_load += 1
        return selected

    def assigned_doctor(self, patient_id: str) -> Doctor | None:
        """Return the patient's currently assigned doctor, if any."""
        target = self._normalise_id(patient_id, "Patient ID")
        doctor_id = self._assignments.get(target)
        return self.find(doctor_id) if doctor_id is not None else None

    def release_patient(self, patient_id: str) -> Doctor:
        """Release a patient's active assignment and return the doctor."""
        target = self._normalise_id(patient_id, "Patient ID")
        doctor_id = self._assignments.get(target)
        if doctor_id is None:
            raise KeyError(f"No active doctor assignment for patient '{target}'.")
        doctor = self.find(doctor_id)
        if doctor is None:
            # Defensive invariant guard: assignments must always reference a registered doctor.
            raise RuntimeError(f"Assigned doctor '{doctor_id}' is missing from the directory.")
        del self._assignments[target]
        doctor._current_load -= 1
        return doctor

    def clear(self) -> None:
        """Clear the directory and all active assignment state."""
        for doctor in self._doctors:
            doctor._current_load = 0
        self._doctors.clear()
        self._assignments.clear()
