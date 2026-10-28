"""Integration tests for the optional FastAPI web adapter.

Install requirements-web.txt before running these tests.
"""
import unittest
from fastapi.testclient import TestClient

from pulseq.api import app, doctors, emergency_queue, patients, routine_queue


class PulseQApiTests(unittest.TestCase):
    def setUp(self) -> None:
        patients.clear()
        routine_queue.clear()
        emergency_queue.clear()
        doctors.clear()
        self.client = TestClient(app)

    def patient_payload(self, patient_id="P1", name="Asha", age=22):
        return {
            "patient_id": patient_id,
            "name": name,
            "age": age,
            "sex": "Prefer not to say",
            "contact": "demo-contact",
            "reason": "Demo visit",
        }

    def create_patient(self, patient_id="P1", name="Asha", age=22):
        return self.client.post("/api/patients", json=self.patient_payload(patient_id, name, age))

    def test_health_and_dashboard(self):
        self.assertEqual(self.client.get("/api/health").status_code, 200)
        result = self.client.get("/api/dashboard")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()["stats"]["patients"], 0)

    def test_seed_demo_workspace_loads_fictional_data_once(self):
        seeded = self.client.post("/api/demo/seed")
        self.assertEqual(seeded.status_code, 200)
        self.assertEqual(len(self.client.get("/api/patients").json()), 5)
        self.assertEqual(len(self.client.get("/api/doctors").json()), 3)
        self.assertEqual(len(self.client.get("/api/routine").json()), 2)
        self.assertEqual(len(self.client.get("/api/emergency").json()), 2)
        self.assertEqual(self.client.post("/api/demo/seed").status_code, 409)

    def test_patient_create_list_update_delete(self):
        created = self.create_patient()
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["patient_id"], "P1")
        self.assertEqual(self.client.patch("/api/patients/P1", json={"age": 23}).json()["age"], 23)
        self.assertEqual(len(self.client.get("/api/patients").json()), 1)
        self.assertEqual(self.client.delete("/api/patients/P1").status_code, 200)
        self.assertEqual(self.client.get("/api/patients").json(), [])

    def test_duplicate_patient_id_returns_client_error(self):
        self.create_patient()
        self.assertEqual(self.create_patient(patient_id="p1").status_code, 400)

    def test_routine_enqueue_and_serve_route_does_not_get_shadowed(self):
        self.create_patient()
        queued = self.client.post("/api/routine/P1/enqueue")
        self.assertEqual(queued.status_code, 201)
        served = self.client.post("/api/routine/serve")
        self.assertEqual(served.status_code, 200)
        self.assertEqual(served.json()["patient_id"], "P1")
        self.assertEqual(self.client.post("/api/routine/serve").status_code, 409)

    def test_patient_cannot_wait_in_both_queues(self):
        self.create_patient()
        self.assertEqual(self.client.post("/api/routine/P1/enqueue").status_code, 201)
        self.assertEqual(self.client.post("/api/emergency/P1/enqueue", json={"urgency": 5}).status_code, 409)

    def test_emergency_heap_serves_higher_demo_urgency_first(self):
        self.create_patient("P1", "Asha")
        self.create_patient("P2", "Bala")
        self.client.post("/api/emergency/P1/enqueue", json={"urgency": 2})
        self.client.post("/api/emergency/P2/enqueue", json={"urgency": 5})
        served = self.client.post("/api/emergency/serve")
        self.assertEqual(served.status_code, 200)
        self.assertEqual(served.json()["patient_id"], "P2")

    def test_doctor_registration_assignment_and_release(self):
        self.create_patient()
        doctor = self.client.post("/api/doctors", json={
            "doctor_id": "DR1", "name": "Dr Nila",
            "specialization": "Cardiology", "contact": "demo-contact",
        })
        self.assertEqual(doctor.status_code, 201)
        assignment = self.client.post("/api/assignments", json={
            "patient_id": "P1", "specialization": "cardiology",
        })
        self.assertEqual(assignment.status_code, 201)
        self.assertEqual(assignment.json()["doctor"]["current_load"], 1)
        self.assertEqual(self.client.delete("/api/assignments/P1").status_code, 200)

    def test_search_and_sort_use_project_algorithms(self):
        self.create_patient("P2", "Bala", 30)
        self.create_patient("P1", "Asha", 22)
        self.assertEqual(self.client.get("/api/search?q=P1&method=binary").json()[0]["patient_id"], "P1")
        sorted_rows = self.client.get("/api/sort?collection=patients&field=age&algorithm=insertion").json()
        self.assertEqual([p["age"] for p in sorted_rows], [22, 30])

    def test_delete_is_blocked_while_patient_waits(self):
        self.create_patient()
        self.client.post("/api/routine/P1/enqueue")
        self.assertEqual(self.client.delete("/api/patients/P1").status_code, 409)


if __name__ == "__main__":
    unittest.main()
