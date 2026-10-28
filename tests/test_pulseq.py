"""Integration tests for PulseQ's menu-driven CLI."""

import unittest

from pulseq.cli import DISCLAIMER, PulseQApp


class InputSequence:
    """Small deterministic input provider for interactive CLI tests."""

    def __init__(self, values: list[str]) -> None:
        self.values = iter(values)

    def __call__(self, prompt: str) -> str:
        try:
            return next(self.values)
        except StopIteration as error:
            raise EOFError from error


class PulseQCliTests(unittest.TestCase):
    def run_app(self, values: list[str]) -> tuple[PulseQApp, str]:
        app = PulseQApp()
        output: list[str] = []
        app.run(input_fn=InputSequence(values), output_fn=output.append)
        return app, "\n".join(output)

    def test_startup_disclaimer_and_clean_exit(self) -> None:
        _, output = self.run_app(["0"])
        self.assertIn(DISCLAIMER, output)
        self.assertIn("Exiting PulseQ", output)

    def test_register_patient_and_view_records(self) -> None:
        app, output = self.run_app([
            "1", "p01", "Asha Rao", "21", "Female", "demo@example.test", "Demo visit",
            "2", "0",
        ])
        self.assertEqual(len(app.patients), 1)
        self.assertIn("Patient P01 registered.", output)
        self.assertIn("P01 | Asha Rao | Age 21", output)

    def test_invalid_menu_choice_reprompts_without_crashing(self) -> None:
        _, output = self.run_app(["abc", "99", "0"])
        self.assertIn("Enter a whole number.", output)
        self.assertIn("Enter a number less than or equal to 17.", output)

    def test_invalid_age_reprompts(self) -> None:
        app, output = self.run_app([
            "1", "P1", "Asha", "not-age", "131", "20", "Female",
            "demo@example.test", "Demo visit", "0",
        ])
        self.assertEqual(len(app.patients), 1)
        self.assertIn("Enter a whole number.", output)
        self.assertIn("Enter a number less than or equal to 130.", output)

    def test_duplicate_patient_id_is_reported_and_app_continues(self) -> None:
        _, output = self.run_app([
            "1", "P1", "Asha", "20", "Female", "demo@example.test", "Demo",
            "1", "p1", "Bala", "21", "Male", "demo@example.test", "Demo",
            "0",
        ])
        self.assertIn("already exists", output)
        self.assertIn("Exiting PulseQ", output)

    def test_routine_queue_uses_registered_patient(self) -> None:
        app, output = self.run_app([
            "1", "P1", "Asha", "20", "Female", "demo@example.test", "Demo",
            "6", "P1", "8", "0",
        ])
        self.assertEqual(len(app.routine_queue), 0)
        self.assertIn("added to the routine FIFO queue", output)
        self.assertIn("Next routine patient: P1 | Asha", output)

    def test_emergency_queue_serves_higher_demo_urgency_first(self) -> None:
        app = PulseQApp()
        app.patients.register(self.make_patient("P1", "Asha"))
        app.patients.register(self.make_patient("P2", "Bala"))
        output: list[str] = []
        app.run(input_fn=InputSequence(["9", "P1", "2", "9", "P2", "5", "11", "0"]), output_fn=output.append)
        self.assertEqual(len(app.emergency_queue), 1)
        self.assertIn("Next by demo priority: P2 | Bala | Score 5", "\n".join(output))

    def test_register_doctor_and_allocate(self) -> None:
        app = PulseQApp()
        app.patients.register(self.make_patient("P1", "Asha"))
        output: list[str] = []
        app.run(
            input_fn=InputSequence([
                "12", "D1", "Dr Demo", "Cardiology", "doctor@example.test",
                "14", "P1", "cardiology", "0",
            ]),
            output_fn=output.append,
        )
        self.assertEqual(app.doctors.assigned_doctor("P1").doctor_id, "D1")
        self.assertIn("Demo assignment: P1 -> D1", "\n".join(output))

    def test_binary_search_and_sort_menu(self) -> None:
        app = PulseQApp()
        app.patients.register(self.make_patient("P2", "Bala"))
        app.patients.register(self.make_patient("P1", "Asha"))
        output: list[str] = []
        app.run(
            input_fn=InputSequence(["3", "3", "p1", "17", "1", "1", "n", "0"]),
            output_fn=output.append,
        )
        rendered = "\n".join(output)
        self.assertIn("P1 | Asha", rendered)
        self.assertIn("Sorted patients display only", rendered)

    def test_emergency_cases_can_be_sorted_by_urgency(self) -> None:
        app = PulseQApp()
        app.patients.register(self.make_patient("P1", "Asha"))
        app.patients.register(self.make_patient("P2", "Bala"))
        output: list[str] = []
        app.run(input_fn=InputSequence(["9", "P1", "2", "9", "P2", "5", "17", "4", "1", "n", "0"]), output_fn=output.append)
        rendered = "\n".join(output)
        p1_position = rendered.rfind("P1 | Asha | Demo urgency 2")
        p2_position = rendered.rfind("P2 | Bala | Demo urgency 5")
        self.assertGreaterEqual(p1_position, 0)
        self.assertGreater(p2_position, p1_position)
        self.assertEqual(len(app.emergency_queue), 2)

    def test_emergency_cases_can_be_sorted_by_arrival_order(self) -> None:
        app = PulseQApp()
        app.patients.register(self.make_patient("P1", "Asha"))
        app.patients.register(self.make_patient("P2", "Bala"))
        output: list[str] = []
        app.run(input_fn=InputSequence(["9", "P1", "2", "9", "P2", "5", "17", "5", "1", "n", "0"]), output_fn=output.append)
        rendered = "\n".join(output)
        p1_position = rendered.rfind("P1 | Asha | Demo urgency 2")
        p2_position = rendered.rfind("P2 | Bala | Demo urgency 5")
        self.assertGreaterEqual(p1_position, 0)
        self.assertGreater(p2_position, p1_position)
        self.assertEqual(len(app.emergency_queue), 2)
    def test_patient_waiting_in_routine_queue_cannot_enter_emergency_queue(self) -> None:
        app = PulseQApp()
        app.patients.register(self.make_patient("P1", "Asha"))
        output: list[str] = []
        app.run(
            input_fn=InputSequence(["6", "P1", "9", "P1", "5", "0"]),
            output_fn=output.append,
        )
        self.assertEqual(len(app.routine_queue), 1)
        self.assertEqual(len(app.emergency_queue), 0)
        self.assertIn(
            "Cannot add to emergency queue: patient is already waiting in the routine queue.",
            "\\n".join(output),
        )

    def test_patient_waiting_in_emergency_queue_cannot_enter_routine_queue(self) -> None:
        app = PulseQApp()
        app.patients.register(self.make_patient("P1", "Asha"))
        output: list[str] = []
        app.run(
            input_fn=InputSequence(["9", "P1", "5", "6", "P1", "0"]),
            output_fn=output.append,
        )
        self.assertEqual(len(app.emergency_queue), 1)
        self.assertEqual(len(app.routine_queue), 0)
        self.assertIn(
            "Cannot add to routine queue: patient is already waiting in the emergency queue.",
            "\\n".join(output),
        )

    def test_delete_is_blocked_for_waiting_patient(self) -> None:
        app = PulseQApp()
        app.patients.register(self.make_patient("P1", "Asha"))
        output: list[str] = []
        app.run(input_fn=InputSequence(["6", "P1", "5", "P1", "0"]), output_fn=output.append)
        self.assertIsNotNone(app.patients.find("P1"))
        self.assertIn("Cannot delete: patient is waiting in the routine queue", "\n".join(output))

    def test_empty_queue_actions_are_friendly(self) -> None:
        _, output = self.run_app(["8", "11", "0"])
        self.assertIn("Routine queue is empty.", output)
        self.assertIn("Emergency priority queue is empty.", output)

    def test_eof_exits_gracefully(self) -> None:
        _, output = self.run_app([])
        self.assertIn("Input ended. Exiting PulseQ.", output)

    @staticmethod
    def make_patient(patient_id: str, name: str):
        from pulseq.models import Patient
        return Patient(
            patient_id=patient_id,
            name=name,
            age=25,
            sex="Unspecified",
            contact="demo@example.test",
            reason="Demo",
        )


if __name__ == "__main__":
    unittest.main()
