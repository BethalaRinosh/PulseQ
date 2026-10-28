"""Menu-driven command-line interface for PulseQ.

This academic prototype uses synthetic demo records only. It is not a real
hospital information system and must not be used for patient-care decisions.
"""

from __future__ import annotations

from collections.abc import Callable

from pulseq.doctors import Doctor, DoctorDirectory
from pulseq.emergency_queue import EmergencyPriorityQueue
from pulseq.models import Patient
from pulseq.patient_store import PatientLinkedList
from pulseq.queues import RoutineQueue
from pulseq.searching import binary_search_by_id, linear_search_by_id, linear_search_by_name
from pulseq.sorting import insertion_sort, merge_sort


DISCLAIMER = (
    "ACADEMIC PROTOTYPE ONLY: PulseQ is a learning simulation. It does not "
    "replace professional medical judgment, validated clinical triage, or a "
    "real hospital information system. Do not use it for real patient-care decisions."
)


class PulseQApp:
    """Own application state and provide a validated text-menu workflow."""

    def __init__(self) -> None:
        self.patients = PatientLinkedList()
        self.routine_queue = RoutineQueue()
        self.emergency_queue = EmergencyPriorityQueue()
        self.doctors = DoctorDirectory()

    @staticmethod
    def _prompt_text(prompt: str, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> str:
        while True:
            value = input_fn(prompt).strip()
            if value:
                return value
            output_fn("Input cannot be empty. Please try again.")

    @staticmethod
    def _prompt_int(
        prompt: str,
        input_fn: Callable[[str], str],
        output_fn: Callable[[str], None],
        *,
        minimum: int | None = None,
        maximum: int | None = None,
    ) -> int:
        while True:
            raw = input_fn(prompt).strip()
            try:
                value = int(raw)
            except ValueError:
                output_fn("Enter a whole number.")
                continue
            if minimum is not None and value < minimum:
                output_fn(f"Enter a number greater than or equal to {minimum}.")
                continue
            if maximum is not None and value > maximum:
                output_fn(f"Enter a number less than or equal to {maximum}.")
                continue
            return value

    def _patient_by_id(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> Patient | None:
        patient_id = self._prompt_text("Patient ID: ", input_fn, output_fn)
        patient = self.patients.find(patient_id)
        if patient is None:
            output_fn(f"No patient found with ID '{patient_id.upper()}'.")
        return patient

    @staticmethod
    def _print_patient(patient: Patient, output_fn: Callable[[str], None]) -> None:
        output_fn(
            f"{patient.patient_id} | {patient.name} | Age {patient.age} | "
            f"{patient.sex} | Contact: {patient.contact} | Reason: {patient.reason}"
        )

    def _register_patient(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        patient = Patient(
            patient_id=self._prompt_text("Patient ID: ", input_fn, output_fn),
            name=self._prompt_text("Full name: ", input_fn, output_fn),
            age=self._prompt_int("Age (0-130): ", input_fn, output_fn, minimum=0, maximum=130),
            sex=self._prompt_text("Sex / gender label: ", input_fn, output_fn),
            contact=self._prompt_text("Contact (use demo data): ", input_fn, output_fn),
            reason=self._prompt_text("Reason for visit (demo only): ", input_fn, output_fn),
        )
        self.patients.register(patient)
        output_fn(f"Patient {patient.patient_id} registered.")

    def _view_patients(self, output_fn: Callable[[str], None]) -> None:
        records = self.patients.view_all()
        if not records:
            output_fn("No patient records yet.")
            return
        for patient in records:
            self._print_patient(patient, output_fn)
        output_fn(f"Total patient records: {len(records)}")

    def _search_patients(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        output_fn("Search: 1) Linear search by ID  2) Partial name search  3) Binary search by ID")
        choice = self._prompt_int("Choose search method: ", input_fn, output_fn, minimum=1, maximum=3)
        if choice == 1:
            query = self._prompt_text("Patient ID: ", input_fn, output_fn)
            found = linear_search_by_id(self.patients.view_all(), query)
            if found is None:
                output_fn("No matching patient.")
            else:
                self._print_patient(found, output_fn)
        elif choice == 2:
            query = self._prompt_text("Name contains: ", input_fn, output_fn)
            matches = linear_search_by_name(self.patients.view_all(), query)
            if not matches:
                output_fn("No matching patients.")
            for patient in matches:
                self._print_patient(patient, output_fn)
        else:
            query = self._prompt_text("Patient ID: ", input_fn, output_fn)
            sorted_records = merge_sort(self.patients.view_all(), key=lambda patient: patient.patient_id)
            found = binary_search_by_id(sorted_records, query)
            if found is None:
                output_fn("No matching patient.")
            else:
                self._print_patient(found, output_fn)

    def _update_patient(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        patient = self._patient_by_id(input_fn, output_fn)
        if patient is None:
            return
        output_fn("Update field: 1) Name  2) Age  3) Sex / gender label  4) Contact  5) Reason for visit")
        field_choice = self._prompt_int("Choose field: ", input_fn, output_fn, minimum=1, maximum=5)
        fields = {1: "name", 2: "age", 3: "sex", 4: "contact", 5: "reason"}
        field = fields[field_choice]
        if field == "age":
            value: object = self._prompt_int("New age (0-130): ", input_fn, output_fn, minimum=0, maximum=130)
        else:
            value = self._prompt_text("New value: ", input_fn, output_fn)
        self.patients.update(patient.patient_id, **{field: value})
        output_fn(f"Patient {patient.patient_id} updated.")

    def _delete_patient(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        patient = self._patient_by_id(input_fn, output_fn)
        if patient is None:
            return
        patient_id = patient.patient_id
        if any(item.patient_id == patient_id for item in self.routine_queue):
            output_fn("Cannot delete: patient is waiting in the routine queue. Serve them first.")
            return
        if any(case.patient.patient_id == patient_id for case in self.emergency_queue.view_all()):
            output_fn("Cannot delete: patient is waiting in the emergency queue. Serve them first.")
            return
        if self.doctors.assigned_doctor(patient_id) is not None:
            output_fn("Cannot delete: release the active doctor assignment first.")
            return
        self.patients.delete(patient_id)
        output_fn(f"Patient {patient_id} deleted.")

    def _enqueue_routine(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        patient = self._patient_by_id(input_fn, output_fn)
        if patient is None:
            return
        if any(item.patient_id == patient.patient_id for item in self.routine_queue):
            output_fn("That patient is already waiting in the routine queue.")
            return
        if any(case.patient.patient_id == patient.patient_id for case in self.emergency_queue.view_all()):
            output_fn("Cannot add to routine queue: patient is already waiting in the emergency queue.")
            return
        self.routine_queue.enqueue(patient)
        output_fn(f"Patient {patient.patient_id} added to the routine FIFO queue.")

    def _view_routine(self, output_fn: Callable[[str], None]) -> None:
        waiting = self.routine_queue.view_all()
        if not waiting:
            output_fn("Routine queue is empty.")
            return
        for position, patient in enumerate(waiting, start=1):
            output_fn(f"{position}. {patient.patient_id} | {patient.name}")
        output_fn(f"Waiting: {len(waiting)}")

    def _serve_routine(self, output_fn: Callable[[str], None]) -> None:
        try:
            patient = self.routine_queue.dequeue()
        except IndexError:
            output_fn("Routine queue is empty.")
            return
        output_fn(f"Next routine patient: {patient.patient_id} | {patient.name}")

    def _enqueue_emergency(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        patient = self._patient_by_id(input_fn, output_fn)
        if patient is None:
            return
        if any(item.patient_id == patient.patient_id for item in self.routine_queue):
            output_fn("Cannot add to emergency queue: patient is already waiting in the routine queue.")
            return
        urgency = self._prompt_int("Demo urgency (1-5, higher is served first): ", input_fn, output_fn, minimum=1, maximum=5)
        self.emergency_queue.enqueue(patient, urgency)
        output_fn(f"Patient {patient.patient_id} added with demo urgency {urgency}. This is not clinical triage.")

    def _view_emergency(self, output_fn: Callable[[str], None]) -> None:
        cases = self.emergency_queue.view_all()
        if not cases:
            output_fn("Emergency priority queue is empty.")
            return
        for position, case in enumerate(cases, start=1):
            output_fn(f"{position}. {case.patient.patient_id} | {case.patient.name} | Demo urgency {case.urgency}")
        output_fn(f"Waiting: {len(cases)}")

    def _serve_emergency(self, output_fn: Callable[[str], None]) -> None:
        try:
            case = self.emergency_queue.dequeue()
        except IndexError:
            output_fn("Emergency priority queue is empty.")
            return
        output_fn(f"Next by demo priority: {case.patient.patient_id} | {case.patient.name} | Score {case.urgency}")
        output_fn("Reminder: this demonstration score is not a clinical triage recommendation.")

    def _register_doctor(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        doctor = Doctor(
            doctor_id=self._prompt_text("Doctor ID: ", input_fn, output_fn),
            name=self._prompt_text("Doctor name: ", input_fn, output_fn),
            specialization=self._prompt_text("Specialization: ", input_fn, output_fn),
            contact=self._prompt_text("Contact (use demo data): ", input_fn, output_fn),
        )
        self.doctors.register(doctor)
        output_fn(f"Doctor {doctor.doctor_id} registered.")

    def _view_doctors(self, output_fn: Callable[[str], None]) -> None:
        doctors = self.doctors.view_all()
        if not doctors:
            output_fn("No doctor records yet.")
            return
        for doctor in doctors:
            state = "Available" if doctor.available else "Unavailable"
            output_fn(
                f"{doctor.doctor_id} | {doctor.name} | {doctor.specialization} | "
                f"{state} | Active demo assignments: {doctor.current_load}"
            )
        output_fn(f"Total doctor records: {len(doctors)}")

    def _allocate_doctor(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        patient = self._patient_by_id(input_fn, output_fn)
        if patient is None:
            return
        specialization = self._prompt_text("Required specialization: ", input_fn, output_fn)
        doctor = self.doctors.allocate_patient(patient, specialization)
        if doctor is None:
            output_fn(f"No available doctor found for specialization '{specialization}'.")
        else:
            output_fn(f"Demo assignment: {patient.patient_id} -> {doctor.doctor_id} ({doctor.name}).")

    def _release_assignment(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        patient_id = self._prompt_text("Patient ID to release: ", input_fn, output_fn)
        try:
            doctor = self.doctors.release_patient(patient_id)
        except KeyError as error:
            output_fn(str(error))
            return
        output_fn(f"Released demo assignment for {patient_id.upper()} from {doctor.doctor_id}.")

    def _toggle_doctor(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        doctor_id = self._prompt_text("Doctor ID: ", input_fn, output_fn)
        doctor = self.doctors.find(doctor_id)
        if doctor is None:
            output_fn(f"No doctor found with ID '{doctor_id.upper()}'.")
            return
        updated = self.doctors.set_availability(doctor_id, not doctor.available)
        state = "available" if updated.available else "unavailable"
        output_fn(f"{updated.doctor_id} is now {state} for new assignments.")

    def _sort_records(self, input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> None:
        output_fn(
            "Sort by: 1) Patient ID  2) Patient name  3) Patient age  "
            "4) Emergency urgency  5) Emergency arrival order"
        )
        field_choice = self._prompt_int("Choose field: ", input_fn, output_fn, minimum=1, maximum=5)
        if field_choice <= 3:
            records = self.patients.view_all()
            if not records:
                output_fn("No patient records to sort.")
                return
            keys = {
                1: lambda patient: patient.patient_id,
                2: lambda patient: patient.name.casefold(),
                3: lambda patient: patient.age,
            }
            key_fn = keys[field_choice]
            record_type = "patients"
        else:
            records = self.emergency_queue.view_all()
            if not records:
                output_fn("No emergency cases to sort.")
                return
            keys = {
                4: lambda case: case.urgency,
                5: lambda case: case.arrival_order,
            }
            key_fn = keys[field_choice]
            record_type = "emergency cases"
        output_fn("Algorithm: 1) Merge sort  2) Insertion sort")
        algorithm_choice = self._prompt_int("Choose algorithm: ", input_fn, output_fn, minimum=1, maximum=2)
        reverse_raw = self._prompt_text("Descending order? (y/n): ", input_fn, output_fn).casefold()
        while reverse_raw not in {"y", "n"}:
            output_fn("Enter y or n.")
            reverse_raw = self._prompt_text("Descending order? (y/n): ", input_fn, output_fn).casefold()
        algorithm = merge_sort if algorithm_choice == 1 else insertion_sort
        sorted_records = algorithm(records, key=key_fn, reverse=reverse_raw == "y")
        if field_choice <= 3:
            for patient in sorted_records:
                self._print_patient(patient, output_fn)
        else:
            for case in sorted_records:
                output_fn(
                    f"{case.patient.patient_id} | {case.patient.name} | "
                    f"Demo urgency {case.urgency} | Arrival order {case.arrival_order}"
                )
        output_fn(f"Sorted {record_type} display only; live queue/storage order is unchanged.")

    def _print_menu(self, output_fn: Callable[[str], None]) -> None:
        output_fn("\n=== PulseQ | Hospital Management & Emergency Response (Academic Demo) ===")
        output_fn(" 1. Register patient        10. View emergency queue")
        output_fn(" 2. View all patients       11. Serve next emergency case")
        output_fn(" 3. Search patients         12. Register doctor")
        output_fn(" 4. Update patient          13. View doctors")
        output_fn(" 5. Delete patient          14. Allocate doctor by specialization")
        output_fn(" 6. Add to routine queue    15. Release doctor assignment")
        output_fn(" 7. View routine queue      16. Toggle doctor availability")
        output_fn(" 8. Serve next routine      17. Sort records")
        output_fn(" 9. Add emergency case       0. Exit")

    def run(
        self,
        input_fn: Callable[[str], str] | None = None,
        output_fn: Callable[[str], None] = print,
    ) -> None:
        """Run until exit or end-of-input. Functions are injectable for tests."""
        read = input if input_fn is None else input_fn
        output_fn(DISCLAIMER)
        actions = {
            1: lambda: self._register_patient(read, output_fn),
            2: lambda: self._view_patients(output_fn),
            3: lambda: self._search_patients(read, output_fn),
            4: lambda: self._update_patient(read, output_fn),
            5: lambda: self._delete_patient(read, output_fn),
            6: lambda: self._enqueue_routine(read, output_fn),
            7: lambda: self._view_routine(output_fn),
            8: lambda: self._serve_routine(output_fn),
            9: lambda: self._enqueue_emergency(read, output_fn),
            10: lambda: self._view_emergency(output_fn),
            11: lambda: self._serve_emergency(output_fn),
            12: lambda: self._register_doctor(read, output_fn),
            13: lambda: self._view_doctors(output_fn),
            14: lambda: self._allocate_doctor(read, output_fn),
            15: lambda: self._release_assignment(read, output_fn),
            16: lambda: self._toggle_doctor(read, output_fn),
            17: lambda: self._sort_records(read, output_fn),
        }
        while True:
            self._print_menu(output_fn)
            try:
                choice = self._prompt_int("Select an option: ", read, output_fn, minimum=0, maximum=17)
                if choice == 0:
                    output_fn("Exiting PulseQ. Demo records are in memory only and have not been saved.")
                    return
                actions[choice]()
            except (ValueError, TypeError, KeyError, AttributeError) as error:
                output_fn(f"Could not complete that action: {error}")
            except EOFError:
                output_fn("\nInput ended. Exiting PulseQ.")
                return
