"""FastAPI adapter for PulseQ's existing in-memory DSA structures.

This API is for local academic demonstrations only. It is not a production
hospital system, and its urgency score is not a clinical triage tool.
"""
from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from pulseq.doctors import Doctor, DoctorDirectory
from pulseq.emergency_queue import EmergencyPriorityQueue
from pulseq.models import Patient
from pulseq.patient_store import PatientLinkedList
from pulseq.queues import RoutineQueue
from pulseq.searching import binary_search_by_id, linear_search_by_id, linear_search_by_name
from pulseq.sorting import insertion_sort, merge_sort

app = FastAPI(
    title="PulseQ API",
    version="1.0.0",
    description="Academic demonstration API backed by custom PulseQ data structures.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

patients = PatientLinkedList()
routine_queue = RoutineQueue()
emergency_queue = EmergencyPriorityQueue()
doctors = DoctorDirectory()


class PatientIn(BaseModel):
    patient_id: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=130)
    sex: str = Field(min_length=1, max_length=40)
    contact: str = Field(min_length=1, max_length=60)
    reason: str = Field(min_length=1, max_length=240)


class PatientPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=0, le=130)
    sex: str | None = Field(default=None, min_length=1, max_length=40)
    contact: str | None = Field(default=None, min_length=1, max_length=60)
    reason: str | None = Field(default=None, min_length=1, max_length=240)


class DoctorIn(BaseModel):
    doctor_id: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=100)
    specialization: str = Field(min_length=1, max_length=80)
    contact: str = Field(min_length=1, max_length=60)


class EmergencyIn(BaseModel):
    urgency: int = Field(ge=1, le=5)


class AssignmentIn(BaseModel):
    patient_id: str = Field(min_length=1, max_length=32)
    specialization: str = Field(min_length=1, max_length=80)


def patient_json(p: Patient) -> dict:
    return {
        "patient_id": p.patient_id,
        "name": p.name,
        "age": p.age,
        "sex": p.sex,
        "contact": p.contact,
        "reason": p.reason,
    }


def doctor_json(d: Doctor) -> dict:
    return {
        "doctor_id": d.doctor_id,
        "name": d.name,
        "specialization": d.specialization,
        "contact": d.contact,
        "available": d.available,
        "current_load": d.current_load,
    }


def emergency_json(case) -> dict:
    return {
        **patient_json(case.patient),
        "urgency": case.urgency,
        "arrival_order": case.arrival_order,
    }


def fail_from_error(error: Exception) -> None:
    if isinstance(error, KeyError):
        raise HTTPException(status_code=404, detail=str(error).strip("'"))
    if isinstance(error, (ValueError, TypeError, AttributeError)):
        raise HTTPException(status_code=400, detail=str(error))
    raise error


def _ensure_not_queued(patient_id: str) -> None:
    if any(p.patient_id == patient_id for p in routine_queue):
        raise HTTPException(status_code=409, detail="Patient is already waiting in the routine queue.")
    if emergency_queue.contains_patient(patient_id):
        raise HTTPException(status_code=409, detail="Patient is already waiting in the emergency queue.")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "PulseQ API", "mode": "in-memory academic demo"}


@app.get("/api/dashboard")
def dashboard() -> dict:
    all_patients = patients.view_all()
    emergencies = emergency_queue.view_all()
    routine = routine_queue.view_all()
    doctor_list = doctors.view_all()
    return {
        "stats": {
            "patients": len(all_patients),
            "routine_waiting": len(routine),
            "emergency_waiting": len(emergencies),
            "doctors": len(doctor_list),
            "doctors_available": sum(1 for d in doctor_list if d.available),
            "active_assignments": sum(d.current_load for d in doctor_list),
        },
        "recent_patients": [patient_json(p) for p in all_patients[-5:][::-1]],
        "routine_next": [patient_json(p) for p in routine[:5]],
        "emergency_next": [emergency_json(c) for c in emergencies[:5]],
        "doctors": [doctor_json(d) for d in doctor_list[:6]],
    }


@app.get("/api/patients")
def list_patients(q: str | None = None) -> list[dict]:
    records = patients.view_all()
    if q and q.strip():
        query = q.strip()
        matches = linear_search_by_name(records, query)
        by_id = linear_search_by_id(records, query)
        if by_id is not None and all(p.patient_id != by_id.patient_id for p in matches):
            matches.insert(0, by_id)
        records = matches
    return [patient_json(p) for p in records]


@app.post("/api/patients", status_code=201)
def create_patient(data: PatientIn) -> dict:
    try:
        patient = Patient(**data.model_dump())
        patients.register(patient)
        return patient_json(patient)
    except (ValueError, TypeError, AttributeError) as error:
        fail_from_error(error)


@app.patch("/api/patients/{patient_id}")
def update_patient(patient_id: str, data: PatientPatch) -> dict:
    changes = {key: value for key, value in data.model_dump(exclude_unset=True).items() if value is not None}
    if not changes:
        raise HTTPException(status_code=400, detail="Provide at least one field to update.")
    try:
        return patient_json(patients.update(patient_id, **changes))
    except (KeyError, ValueError, TypeError, AttributeError) as error:
        fail_from_error(error)


@app.delete("/api/patients/{patient_id}")
def delete_patient(patient_id: str) -> dict:
    patient = patients.find(patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail=f"No patient found with ID '{patient_id.upper()}'.")
    _ensure_not_queued(patient.patient_id)
    if doctors.assigned_doctor(patient.patient_id) is not None:
        raise HTTPException(status_code=409, detail="Release the active doctor assignment before deleting this patient.")
    return patient_json(patients.delete(patient.patient_id))


@app.get("/api/routine")
def list_routine() -> list[dict]:
    return [{"position": i, **patient_json(p)} for i, p in enumerate(routine_queue.view_all(), 1)]


@app.post("/api/routine/{patient_id}", status_code=201)
def add_routine(patient_id: str) -> dict:
    patient = patients.find(patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found.")
    _ensure_not_queued(patient.patient_id)
    routine_queue.enqueue(patient)
    return {"message": f"{patient.patient_id} added to the routine queue.", "patient": patient_json(patient)}


@app.post("/api/routine/serve")
def serve_routine() -> dict:
    try:
        return patient_json(routine_queue.dequeue())
    except IndexError:
        raise HTTPException(status_code=409, detail="The routine queue is empty.")


@app.get("/api/emergency")
def list_emergency() -> list[dict]:
    return [emergency_json(case) for case in emergency_queue.view_all()]


@app.post("/api/emergency/{patient_id}", status_code=201)
def add_emergency(patient_id: str, data: EmergencyIn) -> dict:
    patient = patients.find(patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found.")
    _ensure_not_queued(patient.patient_id)
    try:
        emergency_queue.enqueue(patient, data.urgency)
    except (ValueError, TypeError) as error:
        fail_from_error(error)
    return {"message": f"{patient.patient_id} added with demo urgency {data.urgency}.", "case": emergency_json(emergency_queue.peek())}


@app.post("/api/emergency/serve")
def serve_emergency() -> dict:
    try:
        return emergency_json(emergency_queue.dequeue())
    except IndexError:
        raise HTTPException(status_code=409, detail="The emergency queue is empty.")


@app.get("/api/doctors")
def list_doctors() -> list[dict]:
    return [doctor_json(d) for d in doctors.view_all()]


@app.post("/api/doctors", status_code=201)
def create_doctor(data: DoctorIn) -> dict:
    try:
        doctor = Doctor(**data.model_dump())
        doctors.register(doctor)
        return doctor_json(doctor)
    except (ValueError, TypeError, AttributeError) as error:
        fail_from_error(error)


@app.patch("/api/doctors/{doctor_id}/availability")
def toggle_doctor(doctor_id: str) -> dict:
    doctor = doctors.find(doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found.")
    return doctor_json(doctors.set_availability(doctor_id, not doctor.available))


@app.post("/api/assignments", status_code=201)
def create_assignment(data: AssignmentIn) -> dict:
    patient = patients.find(data.patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found.")
    try:
        doctor = doctors.allocate_patient(patient, data.specialization)
    except (ValueError, TypeError) as error:
        fail_from_error(error)
    if doctor is None:
        raise HTTPException(status_code=409, detail=f"No available doctor for {data.specialization}.")
    return {"patient": patient_json(patient), "doctor": doctor_json(doctor)}


@app.delete("/api/assignments/{patient_id}")
def release_assignment(patient_id: str) -> dict:
    try:
        doctor = doctors.release_patient(patient_id)
        return {"message": f"Released assignment for {patient_id.upper()}.", "doctor": doctor_json(doctor)}
    except KeyError as error:
        fail_from_error(error)


@app.get("/api/search")
def search_patients(q: str = Query(min_length=1), method: Literal["linear", "name", "binary"] = "linear") -> list[dict]:
    records = patients.view_all()
    if method == "name":
        return [patient_json(p) for p in linear_search_by_name(records, q)]
    if method == "binary":
        sorted_records = merge_sort(records, key=lambda p: p.patient_id)
        found = binary_search_by_id(sorted_records, q)
        return [patient_json(found)] if found else []
    found = linear_search_by_id(records, q)
    return [patient_json(found)] if found else []


@app.get("/api/sort")
def sort_records(
    collection: Literal["patients", "emergency"] = "patients",
    field: Literal["id", "name", "age", "urgency", "arrival"] = "id",
    algorithm: Literal["merge", "insertion"] = "merge",
    order: Literal["asc", "desc"] = "asc",
) -> list[dict]:
    reverse = order == "desc"
    sorter = merge_sort if algorithm == "merge" else insertion_sort
    if collection == "patients":
        records = patients.view_all()
        keys = {"id": lambda p: p.patient_id, "name": lambda p: p.name.casefold(), "age": lambda p: p.age}
        if field not in keys:
            raise HTTPException(status_code=400, detail="Patient sort field must be id, name, or age.")
        return [patient_json(p) for p in sorter(records, key=keys[field], reverse=reverse)]
    records = emergency_queue.view_all()
    keys = {"urgency": lambda c: c.urgency, "arrival": lambda c: c.arrival_order}
    if field not in keys:
        raise HTTPException(status_code=400, detail="Emergency sort field must be urgency or arrival.")
    return [emergency_json(c) for c in sorter(records, key=keys[field], reverse=reverse)]
